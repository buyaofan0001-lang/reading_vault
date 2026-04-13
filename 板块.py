import time
from datetime import datetime, timedelta

import akshare as ak
import pandas as pd


# ========== 参数区 ==========
LOOKBACK_DAYS = 300           # 近多少个自然日
USE_TRADING_DAY_FALLBACK = 300  # 如果自然日截取失败，退化为最近多少条交易日
OUTPUT_FILE = "ths_concept_rank_300d.xlsx"
SLEEP_SECONDS = 0.2           # 每次请求间隔，减少接口压力
# ==========================


def safe_to_datetime(series: pd.Series) -> pd.Series:
    """尽量把日期列转成 datetime"""
    return pd.to_datetime(series, errors="coerce")


def normalize_hist_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    兼容 AKShare 不同版本返回字段名
    目标输出字段:
    - date
    - close
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "close"])

    df = df.copy()
    cols = {str(c).strip(): c for c in df.columns}

    date_candidates = ["日期", "date", "Date"]
    close_candidates = ["收盘价", "收盘", "close", "Close"]

    date_col = None
    close_col = None

    for c in date_candidates:
        if c in cols:
            date_col = cols[c]
            break

    for c in close_candidates:
        if c in cols:
            close_col = cols[c]
            break

    if date_col is None or close_col is None:
        raise ValueError(f"历史数据字段无法识别，当前列名为: {list(df.columns)}")

    out = df[[date_col, close_col]].copy()
    out.columns = ["date", "close"]
    out["date"] = safe_to_datetime(out["date"])
    out["close"] = pd.to_numeric(out["close"], errors="coerce")
    out = out.dropna(subset=["date", "close"]).sort_values("date").reset_index(drop=True)
    return out


def get_concept_list() -> pd.DataFrame:
    """
    获取同花顺概念板块列表
    兼容常见字段:
    - 板块名称 / name
    """
    df = ak.stock_board_concept_name_ths()
    if df is None or df.empty:
        raise RuntimeError("未获取到同花顺概念板块列表")

    df = df.copy()
    possible_name_cols = ["板块名称", "name", "概念名称"]
    name_col = None
    for c in possible_name_cols:
        if c in df.columns:
            name_col = c
            break

    if name_col is None:
        raise ValueError(f"无法识别概念板块名称列，当前列名: {list(df.columns)}")

    result = df[[name_col]].copy()
    result.columns = ["name"]
    result = result.dropna().drop_duplicates().reset_index(drop=True)
    return result


def get_concept_hist(name: str) -> pd.DataFrame:
    """
    获取单个同花顺概念板块历史指数
    优先尝试 stock_board_concept_index_ths
    若接口参数风格变化，再尝试其他常见写法
    """
    last_error = None

    # 常见调用 1
    try:
        df = ak.stock_board_concept_index_ths(symbol=name)
        return normalize_hist_df(df)
    except Exception as e:
        last_error = e

    # 常见调用 2，有些版本可能参数名不同
    try:
        df = ak.stock_board_concept_index_ths(name)
        return normalize_hist_df(df)
    except Exception as e:
        last_error = e

    raise RuntimeError(f"{name} 历史数据获取失败: {last_error}")


def calc_return(hist_df: pd.DataFrame, lookback_days: int = 300) -> tuple:
    """
    优先按自然日近300天计算
    若找不到足够接近的起点，则退化为最近300条交易日
    返回:
    start_date, end_date, start_close, end_close, pct_change
    """
    if hist_df.empty or len(hist_df) < 2:
        raise ValueError("历史数据不足")

    hist_df = hist_df.sort_values("date").reset_index(drop=True)
    end_row = hist_df.iloc[-1]
    end_date = end_row["date"]
    end_close = float(end_row["close"])

    target_date = end_date - timedelta(days=lookback_days)
    candidates = hist_df[hist_df["date"] <= target_date]

    if not candidates.empty:
        start_row = candidates.iloc[-1]
    else:
        if len(hist_df) <= USE_TRADING_DAY_FALLBACK:
            start_row = hist_df.iloc[0]
        else:
            start_row = hist_df.iloc[-(USE_TRADING_DAY_FALLBACK + 1)]

    start_date = start_row["date"]
    start_close = float(start_row["close"])

    if start_close == 0:
        raise ZeroDivisionError("起始收盘价为 0，无法计算涨跌幅")

    pct_change = end_close / start_close - 1
    return start_date, end_date, start_close, end_close, pct_change


def main():
    print("开始获取同花顺概念板块列表...")
    concepts = get_concept_list()
    print(f"共获取到 {len(concepts)} 个概念板块")

    rows = []
    failed = []

    for i, row in concepts.iterrows():
        name = row["name"]
        try:
            hist = get_concept_hist(name)
            start_date, end_date, start_close, end_close, pct_change = calc_return(
                hist, lookback_days=LOOKBACK_DAYS
            )

            rows.append(
                {
                    "板块名称": name,
                    "起始日期": start_date.date(),
                    "结束日期": end_date.date(),
                    "起始收盘": start_close,
                    "结束收盘": end_close,
                    "近300天涨跌幅": pct_change,
                }
            )
            print(f"[{i + 1}/{len(concepts)}] 完成: {name}  {pct_change:.2%}")
        except Exception as e:
            failed.append({"板块名称": name, "错误": str(e)})
            print(f"[{i + 1}/{len(concepts)}] 失败: {name}  {e}")

        time.sleep(SLEEP_SECONDS)

    result_df = pd.DataFrame(rows)
    if result_df.empty:
        raise RuntimeError("没有成功获取到任何板块数据，请检查 AKShare 版本或网络环境")

    result_df = result_df.sort_values("近300天涨跌幅", ascending=False).reset_index(drop=True)
    result_df["排名"] = result_df.index + 1
    result_df["近300天涨跌幅_百分比"] = result_df["近300天涨跌幅"].map(lambda x: f"{x:.2%}")

    failed_df = pd.DataFrame(failed)

    # 导出 Excel
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        result_df.to_excel(writer, sheet_name="排名结果", index=False)
        if not failed_df.empty:
            failed_df.to_excel(writer, sheet_name="失败记录", index=False)

    print("\n========== 排名前20 ==========")
    show_cols = ["排名", "板块名称", "起始日期", "结束日期", "近300天涨跌幅_百分比"]
    print(result_df[show_cols].head(20).to_string(index=False))
    print(f"\n已导出到: {OUTPUT_FILE}")

    if not failed_df.empty:
        print(f"有 {len(failed_df)} 个板块获取失败，请查看 Excel 的“失败记录”工作表。")


if __name__ == "__main__":
    main()