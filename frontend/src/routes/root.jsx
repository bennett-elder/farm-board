import { Outlet, Link, useLoaderData } from "react-router-dom";
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
  return (
    <>
      <div id="sidebar">
        <h1><Link to="/">{customPostsName}</Link> ({posts.length})</h1>
        <nav>
          {posts.length ? (
              <table>
                {posts.map((post) => (
                  <tr key={post.id}>
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