import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getOrder } from "../api/orders";
import type { OrderResponse } from "../types/api";

export function OrderResult() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<OrderResponse | null>(null);

  useEffect(() => {
    if (id) getOrder(id).then(setOrder).catch(console.error);
  }, [id]);

  if (!order) return <p>加载中...</p>;
  return (
    <div>
      <h1>订单提交成功</h1>
      <p>订单号：{order.id}</p>
      <p>金额：¥{order.total_amount}</p>
      <p>状态：{order.status}</p>
      <Link to="/">继续购物</Link>
    </div>
  );
}
