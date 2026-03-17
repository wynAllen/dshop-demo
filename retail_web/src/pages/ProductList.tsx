import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getProductList } from "../api/products";
import type { ProductItem } from "../types/api";

export function ProductList() {
  const [items, setItems] = useState<ProductItem[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    getProductList({ page, page_size: 20 })
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
      })
      .catch(console.error);
  }, [page]);

  return (
    <div>
      <h1>商品列表</h1>
      <nav>
        <Link to="/">商品</Link> | <Link to="/cart">购物车</Link>
      </nav>
      <ul>
        {items.map((p) => (
          <li key={p.id}>
            <Link to={`/products/${p.id}`}>{p.name}</Link> — ¥{p.price}
          </li>
        ))}
      </ul>
      {total > 0 && (
        <p>
          第 {page} 页，共 {total} 件
        </p>
      )}
    </div>
  );
}
