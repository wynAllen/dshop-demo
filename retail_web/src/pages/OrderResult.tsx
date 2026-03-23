import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { NavBar } from "../components/NavBar";
import { getOrder } from "../api/orders";
import type { OrderResponse } from "../types/api";

export function OrderResult() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<OrderResponse | null>(null);

  useEffect(() => {
    if (id) getOrder(id).then(setOrder).catch(console.error);
  }, [id]);

  if (!order) {
    return (
      <div className="app">
        <NavBar />
        <p className="loading">加载中...</p>
      </div>
    );
  }
  return (
    <div className="app">
      <NavBar />
      <div className="card" style={{ padding: 32, maxWidth: 420, marginTop: 24 }}>
        <h1 style={{ margin: "0 0 20px", fontSize: "1.35rem" }}>订单提交成功</h1>
        <p style={{ margin: "8px 0" }}><strong>订单号：</strong>{order.id}</p>
        <p style={{ margin: "8px 0" }}><strong>金额：</strong>¥{order.total_amount.toFixed(2)}</p>
        <p style={{ margin: "8px 0" }}><strong>状态：</strong>{order.status}</p>
        <Link to="/" className="btn btn-primary" style={{ marginTop: 24, display: "inline-block" }}>
          继续购物
        </Link>
      </div>
    </div>
  );
}
