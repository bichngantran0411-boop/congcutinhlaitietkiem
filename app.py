import streamlit as st

st.set_page_config(page_title="Công Cụ Tính Lãi Gửi Tiết Kiệm", page_icon="🏦")

st.title("🏦 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.markdown(
    "Ứng dụng tính lãi suất tiết kiệm theo **Lãi Đơn** và **Lãi Kép** "
    "với các hình thức nhận lãi khác nhau."
)
st.divider()

# Hình thức nhận lãi -> số tháng của mỗi chu kỳ (0 = nhận lãi cuối kỳ)
PAYOUT = {
    "Lãnh lãi theo tháng": 1,
    "Lãnh lãi theo quý": 3,
    "Lãnh lãi cuối kỳ": 0,
}

# ---- Nhập liệu ----
col1, col2 = st.columns(2)
with col1:
    principal = st.number_input(
        "1. Số tiền gửi (VND):", min_value=0, value=100_000_000, step=1_000_000
    )
    term = st.number_input("2. Kỳ hạn gửi (tháng):", min_value=1, value=12, step=1)
with col2:
    rate = st.number_input(
        "3. Lãi suất (%/năm):", min_value=0.0, value=6.5, step=0.1, format="%.2f"
    )
    payout = st.selectbox("4. Hình thức nhận lãi:", list(PAYOUT.keys()))

method = st.radio(
    "5. Phương thức tính lãi:",
    ["Lãi Đơn", "Lãi Kép"],
    horizontal=True,
    help="Lãi đơn: chỉ tính lãi trên tiền gốc ban đầu. "
         "Lãi kép: lãi mỗi kỳ được cộng vào gốc để tính lãi cho kỳ sau.",
)

st.divider()

# ---- Tính toán ----
freq = PAYOUT[payout] or term            # số tháng của mỗi chu kỳ
n = term / freq                          # số chu kỳ nhận lãi
period_rate = rate / 100 * freq / 12     # lãi suất của mỗi chu kỳ

if method == "Lãi Đơn":
    period_interest = principal * period_rate
    total_interest = period_interest * n
else:
    period_interest = principal * period_rate           # lãi của chu kỳ đầu tiên
    total_interest = principal * ((1 + period_rate) ** n - 1)

total_amount = principal + total_interest

# ---- Hiển thị kết quả ----
st.header("📊 Kết Quả Dự Tính")
c1, c2, c3 = st.columns(3)
c1.metric(f"Tiền lãi định kỳ ({freq} tháng):", f"{period_interest:,.0f} VND")
c2.metric("Tổng tiền lãi thu về:", f"{total_interest:,.0f} VND")
c3.metric("Tổng gốc + lãi nhận được:", f"{total_amount:,.0f} VND")

st.caption(f"• Tổng thời gian gửi gồm **{n:.1f}** chu kỳ nhận lãi ({freq} tháng/chu kỳ).")

if term % freq != 0:
    st.warning(
        f"Kỳ hạn {term} tháng không chia hết cho {freq} tháng/chu kỳ, "
        "kết quả được tính theo số chu kỳ lẻ."
    )
if payout == "Lãnh lãi cuối kỳ":
    st.info("Nhận lãi cuối kỳ chỉ có 1 chu kỳ nên lãi đơn và lãi kép cho kết quả giống nhau.")
