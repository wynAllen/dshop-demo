export interface ProductItem {
  id: string;
  name: string;
  slug: string;
  description?: string;
  price: number;
  stock: number;
}

export interface ProductListResponse {
  items: ProductItem[];
  total: number;
  page: number;
}

export interface CartItem {
  id: string;
  product_id: string;
  quantity: number;
}

export interface CartResponse {
  items: CartItem[];
}

export interface OrderCreateRequest {
  items: { product_id: string; quantity: number }[];
}

export interface OrderResponse {
  id: string;
  user_id: string;
  total_amount: number;
  status: string;
  items: { product_id: string; quantity: number; price_snapshot: number }[];
}
