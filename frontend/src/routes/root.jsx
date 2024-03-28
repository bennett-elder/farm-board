import { Outlet, Link, useLoaderData } from "react-router-dom";
import moment from "moment";
import { getPosts } from "../data/posts";

export async function loader() {
  const posts = await getPosts();
  console.debug(posts);
  return { posts };
}

export default function Root() {
  const { posts } = useLoaderData();
  return (
    <>
      <div id="sidebar">
        <h1><Link to="/">Farm Board Posts</Link> ({posts.length})</h1>
        <nav>
        <table>
          {posts.length ? (
              <ul>
                {posts.map((post) => (
                  <li key={post.id}>
                    
                      {post.id ? (
                        <tr>
                          <td><Link to={`posts/${post.id}`}>{post.id}</Link></td><td>{moment(post.date).format('MM/DD/YYYY HH:mm')}</td><td>{post.blurb}</td>
                        </tr>
                        
                      ) : (
                        <i>No Name</i>
                      )}{" "}
                    
                  </li>
                ))}
              </ul>
            ) : (
              <p>
                <i>No posts</i>
              </p>
            )}
            </table>
        </nav>
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}