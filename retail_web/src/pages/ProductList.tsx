import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { NavBar } from "../components/NavBar";
import { getProductList } from "../api/products";
import type { ProductItem } from "../types/api";

export function ProductList() {
  const [items, setItems] = useState<ProductItem[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getProductList({ page, page_size: 12 })
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page]);

  const totalPages = Math.ceil(total / 12) || 1;

  return (
    <div className="app">
      <NavBar />
      <h1 style={{ margin: "0 0 24px", fontSize: "1.5rem", fontWeight: 600 }}>商品列表</h1>
      {loading ? (
        <p className="loading">加载中...</p>
      ) : items.length === 0 ? (
        <p className="loading">暂无商品</p>
      ) : (
        <>
          <div className="product-grid">
            {items.map((p) => (
              <Link to={`/products/${p.id}`} key={p.id} className="card product-card">
                <div className="thumb">🛒</div>
                <div className="body">
                  <h2 className="name">{p.name}</h2>
                  <span className="price">¥{p.price.toFixed(2)}</span>
                  <span className="meta">库存 {p.stock} 件</span>
                </div>
              </Link>
            ))}
          </div>
          {total > 12 && (
            <div className="pagination">
              <button
                type="button"
                disabled={page <= 1}
                onClick={() => setPage((prev) => prev - 1)}
              >
                上一页
              </button>
              <span className="page-info">第 {page} / {totalPages} 页，共 {total} 件</span>
              <button
                type="button"
                disabled={page >= totalPages}
                onClick={() => setPage((prev) => prev + 1)}
              >
                下一页
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
