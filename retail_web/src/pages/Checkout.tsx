import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getCart } from "../api/cart";
import { createOrder } from "../api/orders";
import type { CartItem } from "../types/api";

export function Checkout() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const cart = await getCart();
      if (cart.items.length === 0) {
        alert("购物车为空");
        return;
      }
      const order = await createOrder({
        items: cart.items.map((i) => ({ product_id: i.product_id, quantity: i.quantity })),
      });
      navigate(`/orders/${order.id}`);
    } catch (err) {
      console.error(err);
      alert((err as Error).message || "下单失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>收银台</h1>
      <nav>
        <Link to="/">商品</Link> | <Link to="/cart">购物车</Link>
      </nav>
      <form onSubmit={handleSubmit}>
        <button type="submit" disabled={loading}>
          {loading ? "提交中..." : "提交订单"}
        </button>
      </form>
    </div>
  );
}
