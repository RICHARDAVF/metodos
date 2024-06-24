function submit(data,url,callback){
    $.ajax({
        url:url,
        type:"POST",
        conteType:'json',
        data:data,
        processData: false,
        contentType: false,
        success:function(res){
            if(res.error){
                return alert(res.error)
            }
           
            callback(res)
        },
        error:function(xhr,status,error){
            alert(`${status}:${error}`)
        }

    })
}