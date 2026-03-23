import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { NavBar } from "../components/NavBar";
import { getCart } from "../api/cart";
import type { CartItem } from "../types/api";

export function Cart() {
  const { isLoggedIn } = useAuth();
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoggedIn) {
      setLoading(false);
      return;
    }
    getCart()
      .then((res) => setItems(res.items))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [isLoggedIn]);

  return (
    <div className="app">
      <NavBar />
      <h1 style={{ margin: "0 0 24px", fontSize: "1.5rem", fontWeight: 600 }}>购物车</h1>
      {!isLoggedIn ? (
        <div className="cart-page">
          <div className="empty">
            <p>请先登录后查看购物车</p>
            <Link to="/login?redirect=/cart" className="btn btn-primary" style={{ marginTop: 16 }}>
              去登录
            </Link>
          </div>
        </div>
      ) : loading ? (
        <p className="loading">加载中...</p>
      ) : items.length === 0 ? (
        <div className="cart-page">
          <div className="empty">
            <p>购物车是空的</p>
            <Link to="/" className="btn btn-primary" style={{ marginTop: 16 }}>
              去逛逛
            </Link>
          </div>
        </div>
      ) : (
        <div className="cart-page">
          <div className="list">
            {items.map((i) => (
              <div key={i.id} className="item">
                <div className="item-thumb" />
                <div className="item-info">
                  <div className="item-id">商品 ID：{i.product_id}</div>
                  <div className="item-qty">数量：{i.quantity}</div>
                </div>
              </div>
            ))}
          </div>
          <div className="checkout-row">
            <Link to="/checkout" className="btn btn-primary">去结算</Link>
          </div>
        </div>
      )}
    </div>
  );
}
