import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { NavBar } from "../components/NavBar";
import { getCart } from "../api/cart";
import { createOrder } from "../api/orders";
import type { CartItem } from "../types/api";

export function Checkout() {
  const { isLoggedIn } = useAuth();
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

  if (!isLoggedIn) {
    return (
      <div className="app">
        <NavBar />
        <h1 style={{ margin: "0 0 24px", fontSize: "1.5rem", fontWeight: 600 }}>收银台</h1>
        <div className="cart-page">
          <div className="empty">
            <p>请先登录后结算</p>
            <Link to="/login?redirect=/checkout" className="btn btn-primary" style={{ marginTop: 16 }}>
              去登录
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <NavBar />
      <h1 style={{ margin: "0 0 24px", fontSize: "1.5rem", fontWeight: 600 }}>收银台</h1>
      <div className="card" style={{ padding: 24, maxWidth: 400 }}>
        <form onSubmit={handleSubmit}>
          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: "100%" }}>
            {loading ? "提交中..." : "提交订单"}
          </button>
        </form>
      </div>
    </div>
  );
}
