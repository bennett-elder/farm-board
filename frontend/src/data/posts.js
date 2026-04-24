export async function getPosts(query) {
  const response = await fetch(`/post/`);
  const posts = await response.json();
  return posts.sort((a, b) => a.id.localeCompare(b.id));
}

export async function getPostComments(id) {
  const response = await fetch(`/post/${id}`);
  const post = await response.json();
  return post;
}

export async function getCustomPostsName() {
  const response = await fetch(`/config.json`);
  const config = await response.json();
  return config["customPostsName"];
}