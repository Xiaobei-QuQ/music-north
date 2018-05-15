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
                    <a href="./song.html?id=${i.id_}"><li>
                    <h3>${i.name}</h3>
                    <p>${i.singer} - ${i.album}</p>
                   <svg>
                    <use xlink:href="#icon-play1"></use>
                    </svg></li></a>
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
    $('input#searchSong').on('click',function () {
        $('.searchWrap i .icon-cancel').addClass('active')
        $('.output').addClass('active')
    })
    let timer = undefined
    $('input#searchSong').on('input propertychange',function (e) {
        $('.output a').remove()
        let $input = $(e.currentTarget)
        let value = $input.val().trim()
        $('.showSearch').text("搜索：\""+value+"\"")
        console.log(value)
        if(value == ''){return}
        if(timer){
            clearTimeout(timer)
        }
        timer = setTimeout(function () {
            search(value).then((result)=>{
                timer = undefined
                if(result.length !== 0){
                let outValue = result
                outValue.forEach((i)=>{
                    let outText = ` 
                        <a href="./song.html?id=${i.id_}"><li>
                            <i>
                            <svg class="icon-search">
                                <use xlink:href="#icon-search"></use>
                            </svg>
                            </i>
                            <span>${i.name}-${i.singer}</span>
                        </li></a>
                `
                    $('.output ol').append(outText)
                })

                }else{
                    let noOut = `
                    <a><li><span>无搜索结果</span</li></a>
                    `
                    $('.output ol').append(noOut)
                }
            })
        },300)
    })
    $('.searchWrap i .icon-cancel').on('click',function () {
        $('input#searchSong').val('')
    })
    function search(keyword) {
            return new Promise((resolve, reject) => {
                $.get('./data/播放列表.json').then((response)=>{
                    let database = response
                    let result1 = database.filter(function (item) {
                        return item.name.indexOf(keyword) >=0
                    })
                    let result2 = database.filter(function (item) {
                        return item.singer.indexOf(keyword) >=0
                    })
                    let result = result1.concat(result2)
                    console.log(result)
                    setTimeout(function () {
                        resolve(result)
                    },(Math.random() * 300 + 1000)
                    )
                })
            })
    }
    function hotSonglist(response) {
        let items = response
        let index = 0
        items.forEach((i)=>{
            index++
            if(index<10){index = '0'+ index}
            let $li =$(`
                    <li><span>${index}</span>
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
    let date = new Date()
    let month =  date.getMonth()+1
    let day = date.getDate()
    console.log(day)
    $('.hot-title .hot-time').text('更新时间：'+month+'月'+day+'日')
})
