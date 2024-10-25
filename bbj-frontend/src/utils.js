import axios from "axios";

async function getCurrentUser(that){
    var res = await axios.get("/api/checkLoginState", {
        withCredentials: true,
        headers: {
            "content-type": "application/json",
            'X-CSRFTOKEN': that.$cookies.get("csrftoken")
        }
    })

    if(res.data["isLogged"]) {
        console.log(res.data['userName'])
        return res.data
    }else{
        return "Anonymous"
    }
}

export {getCurrentUser}