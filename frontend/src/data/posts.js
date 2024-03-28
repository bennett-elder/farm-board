import sortBy from "sort-by";

export async function getPosts(query) {
  const response = await fetch(`/post/`);
  const posts = await response.json();
  return posts.sort(sortBy("id"));
}

export async function getPostComments(id) {
  const response = await fetch(`/post/${id}`);
  const post = await response.json();
  return post;
}
