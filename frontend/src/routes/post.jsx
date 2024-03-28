import { Form, useLoaderData } from "react-router-dom";
import moment from "moment";
import { getPostComments } from "../data/posts";

let id = "";

export async function loader({ params }) {
  const comments = await getPostComments(params.id);
  id = params.id;
  return { comments };
}

export default function Post() {
  const { comments } = useLoaderData();

  return (
    <div id="post">

      <div>
        <h1>
          {id ? (
            <>
              {id}
            </>
          ) : (
            <i>No Name</i>
          )}{" "}
        </h1>

        <table>
        {
          comments.map((comment, index) => {
            return (
              <tr key={index}>
              <td>{moment(comment.date).format('MM/DD/YYYY HH:mm')}</td><td>{comment.blurb}</td>
              </tr>
            )
          })
        }
        </table>
      </div>
    </div>
  );
}
