import { useEffect, useState } from "react"


function App() {
    const [posts, setPosts] = useState([])
    const [board, setBoard] = useState([])

    useEffect(() => {
        const fetchAllPosts = async () => {
            const response = await fetch("/post/")
            const fetchedPosts = await response.json()
            setPosts(fetchedPosts)
        }

        const interval = setInterval(fetchAllPosts, 1000)

        return () => {
            clearInterval(interval)
        }
    }, [])

    useEffect(() => {
        const boardItems = posts.reverse().map((post) => {
            return <p>{post.date} - {post.id} - {post.blurb}</p>
        })

        setBoard(boardItems)
    }, [posts])

    return (
        <>
            <div>{board}</div>
        </>
    )
}

export default App
