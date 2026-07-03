import streamlit as st
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="赣州富硒农产品产销便民服务平台", layout="wide")
st.title("赣州富硒农产品产销便民服务平台")

# 全局加载CSV数据，提前定义df，解决变量未定义报错
df = pd.read_csv("data.csv")
st.success("数据加载完成，可切换下方板块查看对应内容")

# 左侧身份下拉选择框
identity = st.selectbox("请选择您的身份", ["消费者（购买用户）", "经销商（收购商）", "农户（种植户）"])

# ========== 消费者页面逻辑 ==========
if identity == "消费者（购买用户）":
    st.header("🛒 消费者产品选购专区")
    st.subheader("全部富硒农产品介绍与售价")
    # 筛选消费者展示字段
    consumer_df = df[["产品名称", "产品品类", "产地", "单价（元/斤）", "富硒等级", "供货状态"]]
    st.dataframe(consumer_df, use_container_width=True)

# ========== 经销商页面逻辑 ==========
elif identity == "经销商（收购商）":
    st.header("🤝 经销商收购参考专区")
    st.subheader("全部富硒农产品产地、单价、供货销量明细")
    dealer_df = df[["产品名称", "产品品类", "产地", "单价（元/斤）", "月度供货量"]]
    st.dataframe(dealer_df, use_container_width=True)
    st.info("提示：您可以横向对比不同县城同款农产品的售价，选择性价比更高的货源收购。")

# ========== 农户页面逻辑 ==========
elif identity == "农户（种植户）":
    st.header("👨‍🌾 农户种植参考专区")
    st.subheader("各县农产品月度总销量统计表（用来判断今年种什么更好卖）")
    # 按产地分组统计总销量
    farmer_data = df.groupby("产地")["月度供货量"].sum().reset_index()
    farmer_data.columns = ["种植产地（县城）", "月度总销量"]
    st.dataframe(farmer_data, use_container_width=True)
    st.info("提示：表格里销量越高的农产品品类，市场需求越大，您可以优先规划种植这类作物，减少滞销风险。")
