import "./index.css"
import Root, { loader as rootLoader } from "./routes/root";

import React from "react"
import ReactDOM from "react-dom"
import {
    createBrowserRouter,
    RouterProvider,
    useLoaderData,
} from "react-router-dom";
import ErrorPage from "./error-page";
import Post, {
    loader as postLoader,
  } from "./routes/post";

const router = createBrowserRouter([
    {
      path: "/",
      element: <Root />,
      errorElement: <ErrorPage />,
      loader: rootLoader,
      children: [
        {
          path: "posts/:id",
          element: <Post />,
          loader: postLoader
        },
      ],
    },
    // {
    //     path: "posts/:id",
    //     element: <Post />,
    //     loader: postLoader
    // },
]);
  
ReactDOM.render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>,
    document.getElementById("root")
)