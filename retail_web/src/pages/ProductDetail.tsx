import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { NavBar } from "../components/NavBar";
import { getProductById } from "../api/products";
import { addCartItem } from "../api/cart";
import type { ProductItem } from "../types/api";

export function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isLoggedIn } = useAuth();
  const [product, setProduct] = useState<ProductItem | null>(null);
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    if (id) {
      getProductById(id).then(setProduct).catch(console.error);
    }
  }, [id]);

  const handleAddCart = () => {
    if (!product) return;
    if (!isLoggedIn) {
      navigate(`/login?redirect=${encodeURIComponent(window.location.pathname)}`);
      return;
    }
    setAdding(true);
    addCartItem(product.id, 1)
      .then(() => {
        if (window.confirm("已加入购物车，是否前往购物车？")) {
          navigate("/cart");
        }
      })
      .catch(console.error)
      .finally(() => setAdding(false));
  };

  if (!product) {
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
      <div className="product-detail-page">
        <Link to="/" className="back">← 返回商品列表</Link>
        <div className="main">
          <div className="thumb-lg">🛒</div>
          <div className="info">
            <h1>{product.name}</h1>
            <p className="price">¥{product.price.toFixed(2)}</p>
            {product.description && (
              <p className="desc">{product.description}</p>
            )}
            <p className="stock">库存：{product.stock} 件</p>
            {!isLoggedIn ? (
              <p style={{ color: "var(--color-text-muted)", marginBottom: 12 }}>
                请先 <Link to={`/login?redirect=${encodeURIComponent(`/products/${id}`)}`}>登录</Link> 后再加入购物车
              </p>
            ) : null}
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleAddCart}
              disabled={adding || product.stock < 1 || !isLoggedIn}
            >
              {adding ? "加入中..." : "加入购物车"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
