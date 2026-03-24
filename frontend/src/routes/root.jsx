import { Outlet, Link, useLoaderData } from "react-router-dom";
import { useState } from "react";
import moment from "moment";
import { getPosts, getCustomPostsName } from "../data/posts";

export async function loader() {
  const posts = await getPosts();
  console.debug(posts);
  const customPostsName = await getCustomPostsName();
  return { posts, customPostsName };
}

export default function Root() {
  const { posts, customPostsName } = useLoaderData();
  const [filter, setFilter] = useState("");

  const filtered = posts.filter((post) => {
    const q = filter.toLowerCase();
    return (
      post.id.toLowerCase().includes(q) ||
      post.blurb.toLowerCase().includes(q) ||
      moment(post.date).format('MM/DD/YYYY HH:mm').includes(q)
    );
  });

  return (
    <>
      <div id="sidebar">
        <h1><Link to="/">{customPostsName}</Link> ({posts.length})</h1>
        <input
          id="filter"
          type="text"
          placeholder="Filter..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        <nav>
          {filtered.length ? (
              <table>
                {filtered.map((post) => (
                  <tr key={post.id} className={moment().diff(moment(post.date), 'days') > 7 ? 'stale' : ''}>
                      <td><Link to={`posts/${post.id}`}>{post.id}</Link></td><td>{moment(post.date).format('MM/DD/YYYY HH:mm')}</td><td>{post.blurb}</td>
                  </tr>
                ))}
              </table>
            ) : (
              <p>
                <i>No posts</i>
              </p>
            )}
        </nav>
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}