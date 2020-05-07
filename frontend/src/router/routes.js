const routes = [
  {
    path: "",
    redirect: "/home",
  },
  {
    path: "",
    component: () => import("layouts/LoggedInLayout.vue"),
    meta: { requiresAuth: true },
    children: [
      { path: "/home", component: () => import("pages/HomePage.vue") },
      {
        path: "/transactions/all",
        component: () => import("pages/TransactionsPage.vue"),
      },
      {
        path: "/transactions",
        component: () => import("pages/TransactionMonthPage.vue"),
      },
      {
        path: "/categories",
        component: () => import("pages/CategoriesPage.vue"),
      },
    ],
  },
  {
    path: "/login",
    component: () => import("pages/LoginPage.vue"),
    children: [],
  },
];

// Always leave this as last one
if (process.env.MODE !== "ssr") {
  routes.push({
    path: "*",
    component: () => import("pages/Error404.vue"),
  });
}

export default routes;
