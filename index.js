$(function(){
    // $.get('./songs.json').then(function (res) {
    //     let items = res
    //     items.forEach((i)=>{
    //             let $li =$(`
    //                 <li>
    //                 <a href="./song.html?id=${i.id}">
    //                 <h3>${i.title}</h3>
    //                 <p>${i.author}</p>
    //                <svg>
    //                 <use xlink:href="#icon-play1"></use>
    //                 </svg></a></li>
    //             </ol>
    //             `)
    //             $('#latesMusic').append($li)
    //         })
    //         $('.musicLoading').remove()
    // })
    $.get('./otherSongs.json').then(function (res) {
        let items = res
        items.forEach((i)=>{
            let $li =$(`
                    <li>
                    <a href="./song.html?id=${i.id_}">
                    <h3>${i.name}</h3>
                    <p>${i.album} ${i.signer}</p>
                   <svg>
                    <use xlink:href="#icon-play1"></use>
                    </svg></a></li>
                </ol>
                `)
            $('#latesMusic').append($li)
    })
        $('.musicLoading').remove()
    })
})
