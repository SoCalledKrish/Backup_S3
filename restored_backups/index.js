const express = require ("express");
const app = express();

app.use(express.json());

app.get("/", (req, res)=>{
    res.send("Hello Moron");
});

app.post("/", (req,res)=>{
    console.log(req.body);
    res.send("Got a post req");
})

app.put("/user", (req,res)=>{
    console.log(req.body)
    res.send(" Got a put request at /user")
})

app.delete("/user", (req,res)=>{
    console.log(req.body);
    res.send("Got a delete request at /user");
})

app.get("/users/*", (req,res)=>{
    console.log(req.body);
    res.send("Got all the requests of users");
})


app.get("/user/:id", (req,res)=>{
    let id = req.params["id"];
    res.send("This is the id: "+ id);
})

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server started on port ${3000}`));
