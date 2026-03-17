import type { OrderCreateRequest, OrderResponse } from "../types/api";
import { apiFetch } from "./client";

export function createOrder(body: OrderCreateRequest): Promise<OrderResponse> {
  return apiFetch<OrderResponse>("/api/v1/orders", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function getOrder(orderId: string): Promise<OrderResponse> {
  return apiFetch<OrderResponse>(`/api/v1/orders/${orderId}`);
}
