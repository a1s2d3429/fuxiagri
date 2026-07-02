import pandas as pd
import pymysql
import streamlit as st

# 页面全局设置
st.set_page_config(page_title="赣州富硒农产品产销服务平台", layout="wide")
st.title("赣州富硒农产品产销便民服务平台")

# ========== 1. 连接数据库读取数据（修改mysql账号密码即可） ==========
@st.cache_data
def load_data():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="HZRhzr142857",  # 修改这里
        database="se_agricultural",  # 修改这里
        charset="utf8mb4"
    )
    df = pd.read_sql("SELECT * FROM sheet1", conn)
    conn.close()
    # 销量转为数字，防止计算报错
    df["月度销量"] = pd.to_numeric(df["月度销量"], errors="coerce")
    return df

# 加载数据
try:
    df = load_data()
    st.success("数据加载完成，可切换下方板块查看对应内容")
except Exception as e:
    st.error(f"数据库连接失败，请核对账号信息：{e}")

# ========== 2. 侧边栏切换三大板块 ==========
menu = st.sidebar.selectbox("请选择您的身份", ["农户（种植户）", "经销商（收购商）", "消费者（购买用户）"])

# ========== 3. 农户专区：查看销量，规划种植 ==========
if menu == "农户（种植户）":
    st.header("👨‍🌾 农户种植参考专区")
    st.subheader("各县农产品月度总销量统计表（用来判断今年种什么更好卖）")
    # 按产地汇总销量
    farmer_data = df.groupby("产地")["月度销量"].sum().reset_index()
    farmer_data.columns = ["种植产地（县城）", "月度总销量"]
    st.dataframe(farmer_data, use_container_width=True)
    # 通俗提示
    st.info("提示：表格里销量越高的农产品品类，市场需求越大，您可以优先规划种植这类作物，减少滞销风险。")

# ========== 4. 经销商专区：查看全部产品价格、供货量 ==========
elif menu == "经销商（收购商）":
    st.header("🤝 经销商收购参考专区")
    st.subheader("全部富硒农产品产地、单价、供货销量明细")
    dealer_data = df[["产品名称", "产品分类", "产地", "单价", "月度销量"]]
    dealer_data.columns = ["农产品名称", "产品品类", "产地县城", "单斤售价", "月度供货量"]
    st.dataframe(dealer_data, use_container_width=True)
    st.info("提示：您可以横向对比不同县城同款农产品的售价，选择性价比更高的货源收购。")

# ========== 5. 消费者专区：产品详情+价格+购买说明 ==========
elif menu == "消费者（购买用户）":
    st.header("🛒 消费者产品选购专区")
    st.subheader("全部富硒农产品介绍与售价")
    customer_data = df[["产品名称", "产品分类", "产地", "单价", "富硒等级", "上市季节"]]
    customer_data.columns = ["产品名称", "产品品类", "产地", "单价（元/斤）", "富硒等级", "供货状态"]
    st.dataframe(customer_data, use_container_width=True)
    # 购买途径文字说明
    st.subheader("📦 线下线上购买途径")
    st.write("1. 线下：赣州各区县农贸市场、本地生鲜超市、富硒农产品线下展销门店")
    st.write("2. 线上：本地电商小程序、助农直播平台、赣州农产品官方线上商城")
    st.info("提示：供货状态显示正常即可选购，富硒等级越高，产品硒元素含量越优质。")
