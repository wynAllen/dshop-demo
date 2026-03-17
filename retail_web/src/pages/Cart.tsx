import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getCart } from "../api/cart";
import type { CartItem } from "../types/api";

export function Cart() {
  const [items, setItems] = useState<CartItem[]>([]);

  useEffect(() => {
    getCart()
      .then((res) => setItems(res.items))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1>购物车</h1>
      <nav>
        <Link to="/">商品</Link> | <Link to="/cart">购物车</Link>
      </nav>
      <ul>
        {items.map((i) => (
          <li key={i.id}>
            product_id: {i.product_id}, 数量: {i.quantity}
          </li>
        ))}
      </ul>
      {items.length > 0 && (
        <Link to="/checkout">去结算</Link>
      )}
    </div>
  );
}
