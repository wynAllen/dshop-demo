import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ProductList } from "./pages/ProductList";
import { ProductDetail } from "./pages/ProductDetail";
import { Cart } from "./pages/Cart";
import { Checkout } from "./pages/Checkout";
import { OrderResult } from "./pages/OrderResult";
import { AdminPlaceholder } from "./pages/AdminPlaceholder";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/products/:id" element={<ProductDetail />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/orders/:id" element={<OrderResult />} />
        <Route path="/admin/*" element={<AdminPlaceholder />} />
      </Routes>
    </BrowserRouter>
  );
}
