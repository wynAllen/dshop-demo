import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getProductById } from "../api/products";
import { addCartItem } from "../api/cart";
import type { ProductItem } from "../types/api";

export function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<ProductItem | null>(null);

  useEffect(() => {
    if (id) {
      getProductById(id).then(setProduct).catch(console.error);
    }
  }, [id]);

  const handleAddCart = () => {
    if (!product) return;
    addCartItem(product.id, 1).then(() => alert("已加入购物车")).catch(console.error);
  };

  if (!product) return <p>加载中...</p>;
  return (
    <div>
      <nav>
        <Link to="/">商品</Link> | <Link to="/cart">购物车</Link>
      </nav>
      <h1>{product.name}</h1>
      <p>¥{product.price}</p>
      {product.description && <p>{product.description}</p>}
      <button type="button" onClick={handleAddCart}>
        加入购物车
      </button>
    </div>
  );
}
