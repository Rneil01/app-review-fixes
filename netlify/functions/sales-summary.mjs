// Read-only sales summary for Alex's Analyst. Requires ?key=SALES_KEY. Returns totals only (no personal data).
import { getStore } from "@netlify/blobs";

export default async (req) => {
  const url = new URL(req.url);
  const key = Netlify.env.get("SALES_KEY");
  if (!key || url.searchParams.get("key") !== key) return new Response("forbidden", { status: 403 });

  const store = getStore("sales");
  const { blobs } = await store.list({ prefix: "sale/" });
  const sales = [];
  for (const b of blobs) {
    const r = await store.get(b.key, { type: "json" });
    if (r) sales.push(r);
  }
  const real = sales.filter((s) => !s.test);
  const live = real.filter((s) => !s.refunded);
  const byProduct = {};
  const revenueCents = {};
  for (const s of live) {
    byProduct[s.product_name] = (byProduct[s.product_name] || 0) + (s.quantity || 1);
    revenueCents[s.currency] = (revenueCents[s.currency] || 0) + s.price;
  }
  live.sort((a, b) => String(b.sale_timestamp).localeCompare(String(a.sale_timestamp)));
  const body = {
    generated_at: new Date().toISOString(),
    sales_count: live.length,
    refunded_count: real.length - live.length,
    test_pings: sales.length - real.length,
    gross_revenue_cents_by_currency: revenueCents,
    sales_by_product: byProduct,
    recent: live.slice(0, 10).map((s) => ({ product: s.product_name, price_cents: s.price, currency: s.currency, at: s.sale_timestamp })),
  };
  return new Response(JSON.stringify(body, null, 2), {
    headers: { "content-type": "application/json", "cache-control": "no-store", "x-robots-tag": "noindex" },
  });
};

export const config = { path: "/api/sales-summary" };
