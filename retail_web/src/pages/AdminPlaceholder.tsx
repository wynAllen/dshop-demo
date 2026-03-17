import { Link } from "react-router-dom";

export function AdminPlaceholder() {
  return (
    <div>
      <h1>管理后台</h1>
      <aside>
        <Link to="/admin">首页</Link>
        <br />
        <Link to="/admin/products">商品管理</Link>
        <br />
        <Link to="/admin/orders">订单管理</Link>
      </aside>
      <p>占位页，后续实现。</p>
    </div>
  );
}
