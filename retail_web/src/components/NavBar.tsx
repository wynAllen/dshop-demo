import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function NavBar() {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="nav">
      <Link to="/" className="brand">dShop 零售</Link>
      <Link to="/">商品</Link>
      <Link to="/cart">购物车</Link>
      {isLoggedIn ? (
        <button type="button" className="logout" onClick={handleLogout}>
          退出
        </button>
      ) : (
        <>
          <Link to="/login">登录</Link>
          <Link to="/register">注册</Link>
        </>
      )}
    </nav>
  );
}
