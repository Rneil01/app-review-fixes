// Receives Gumroad "Ping" notifications (one POST per sale) and stores one record per sale.
// Gumroad: Settings > Advanced > Ping endpoint = https://app-review-fixes.netlify.app/api/gumroad-ping?key=SALES_KEY
import { getStore } from "@netlify/blobs";

export default async (req) => {
  const url = new URL(req.url);
  const key = Netlify.env.get("SALES_KEY");
  if (!key || url.searchParams.get("key") !== key) return new Response("forbidden", { status: 403 });
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });

  const form = await req.formData();
  const saleId = String(form.get("sale_id") || "").replace(/[^A-Za-z0-9_=-]/g, "");
  if (!saleId) return new Response("missing sale_id", { status: 400 });

  // Store only what's needed for reporting. No buyer email or personal data.
  const record = {
    sale_id: saleId,
    product_name: String(form.get("product_name") || ""),
    permalink: String(form.get("permalink") || ""),
    price: Number(form.get("price") || 0), // Gumroad sends price in cents
    currency: String(form.get("currency") || "usd"),
    quantity: Number(form.get("quantity") || 1),
    sale_timestamp: String(form.get("sale_timestamp") || new Date().toISOString()),
    refunded: String(form.get("refunded") || "false") === "true",
    test: String(form.get("test") || "false") === "true",
    received_at: new Date().toISOString(),
  };
  await getStore("sales").setJSON(`sale/${saleId}`, record);
  return new Response("ok");
};

export const config = { path: "/api/gumroad-ping" };
