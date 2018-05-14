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
    $.get('./data/最新音乐.json').then(function (res) {
        let items = res
        items.forEach((i)=>{
            let $li =$(`
                    <li>
                    <a href="./song.html?id=${i.id_}">
                    <h3>${i.name}</h3>
                    <p>${i.signer} - ${i.album}</p>
                   <svg>
                    <use xlink:href="#icon-play1"></use>
                    </svg></a></li>
                </ol>
                `)
            $('#latesMusic').append($li)
        })
        $('.musicLoading').remove()
    })
    $('.siteNav').on('click','ol.tabItems>li',function (e) {
        let $li = $(e.currentTarget).addClass('active')
        $li.siblings().removeClass('active')
        let index = $li.index()
        $li.trigger('tabChange',index)
        $('.tabContent > ol > li').eq(index).addClass('active')
            .siblings().removeClass('active')
    })
    $('.siteNav').on('tabChange',function (e,index) {
        let $li = $('.tabContent > ol > li').eq(index)
        if($li.attr('data-downloaded') === 'yes') {
            return
        }
         if(index === 1) {
            $.get('./data/热歌榜.json').then((response)=>{
                hotSonglist(response)
                $li.attr('data-downloaded','yes')
                $('.tab2Loading').remove()
         })
        }else if(index === 2){
            $.get('./data/page3.json').then((response)=>{
                $li.text(response.content)
                $li.attr('data-downloaded','yes')
             $('.tab3Loading').remove()
            })
        }
    })
    let timer = undefined
    $('input#searchSong').on('input',function (e) {
        let $input = $(e.currentTarget)
        let value = $input.val().trim()
        console.log(value)
        if(value === undefined){return}
        if(timer){
            clearTimeout(timer)
        }
        timer = setTimeout(function () {
            search(value).then((result)=>{
                timer = undefined
                if(result.length !== 0){
                    console.log(result)
                    $('.output').text(result.map(r=>r.name).join(','))
                }else{
                    $('.output').text('没有结果')
                }
            })
        },300)
    })

    function search(keyword) {
            return new Promise((resolve, reject) => {
                var database = [
                    {"id": 1, "name": "那些花儿"},
                    {"id": 2, "name": "情非得已"},
                    {"id": 3, "name": "找自己"}
                ]
                let result = database.filter(function (item) {
                    return item.name.indexOf(keyword) >= 0
                })
                setTimeout(function () {
                    resolve(result)
                },(Math.random() * 300 + 1000)
                )
            })
    }
    function hotSonglist(response) {
        let items = response
        items.forEach((i)=>{
            let $li =$(`
                    <li>
                    <a href="./song.html?id=${i.id_}">
                    <h3>${i.name}</h3>
                    <p>${i.singer} - ${i.album}</p>
                   <svg>
                    <use xlink:href="#icon-play1"></use>
                    </svg></a>
                    </li>
                `)
            $('#hotSonglist').append($li)
        })
    }
})
