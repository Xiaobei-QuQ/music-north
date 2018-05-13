$(function(){
     let id = location.search.match(/\bid=([^&]*)/)[1]
    // $.get('./songs.json').then(
    //     function (res) {
    //         let songs = res
    //         let song = songs.filter(s=>s.id === id)[0]
    //         let {src} = song
    //         let audio = document.createElement('audio')
    //         audio.src = src
    //             // 'http://link.hhtjim.com/163/551337740.mp3'
    //         var cover = $('.disc-container .cover')
    //         if ( cover.css('animation-play-state') === 'running' ) {
    //             cover.css('animation-play-state','paused')
    //         }
    //         audio.setAttribute('autoplay','autoplay')
    //         audio.setAttribute('volume','0')
    //         audio.oncanplay = function(){
    //             audio.play()
    //             $('.disc-container').addClass('playing')
    //             cover.css('animation-play-state','running')
    //         }
    //         $('.icon-pause').on('click',function () {
    //             audio.pause()
    //             $('.disc-container').removeClass('playing')
    //             cover.css('animation-play-state','paused')
    //         })
    //         $('.icon-play').on('click',function () {
    //             audio.play()
    //             $('.disc-container').addClass('playing')
    //             cover.css('animation-play-state','running')
    //
    //         })
    //     }
    // )
    $.get('./newData.json').then(
        function (res) {
            let songs = res
            let song = songs.filter(s=>s.id_ == id)[0]
            let {id_,name,album,signer,lyric,album_pic} = song
            url = 'http://link.hhtjim.com/163/'+parseInt(id_)+'.mp3'
            initPlayer.call(undefined,url)
            initText(name,lyric)
            console.log(lyric)
            parseLyric.call(undefined,lyric)
            setBg(album_pic)
            console.log(album_pic)
        }
    )
    function setBg(album_pic) {
        $('.disc-container .cover').attr('src',album_pic)
    }
    function initPlayer(url) {
        let audio = document.createElement('audio')
        audio.src = url
        // 'http://link.hhtjim.com/163/551337740.mp3'
        var cover = $('.disc-container .cover')
        if ( cover.css('animation-play-state') === 'running' ) {
            cover.css('animation-play-state','paused')
        }
        audio.setAttribute('autoplay','autoplay')
        audio.setAttribute('volume','0')
        audio.oncanplay = function(){
            audio.play()
            $('.disc-container').addClass('playing')
            cover.css('animation-play-state','running')
        }
        $('.icon-pause').on('click',function () {
            audio.pause()
            $('.disc-container').removeClass('playing')
            cover.css('animation-play-state','paused')
        })
        $('.icon-play').on('click',function () {
            audio.play()
            $('.disc-container').addClass('playing')
            cover.css('animation-play-state','running')
        })
        setInterval(()=>{
            let seconds = audio.currentTime
            let munites = ~~(seconds / 60)
            let left = seconds - munites*60
            let time = `${pad(munites)}:${pad(left)}`
            let $lines = $('.lines>p')
            let $whichLine
            for(let i = 0;i< $lines.length;i++){
                if($lines[i+1]!== undefined && $lines.eq(i).attr('data-time')< time && $lines.eq(i+1).attr('data-time')>time){
                    $whichLine = $lines.eq(i)
                    break
                }
            }
            if($whichLine){
                $whichLine.addClass('active').prev().removeClass('active')
                let top = $whichLine.offset().top
                let linesTop = $('.lines').offset().top
                let delta = top - linesTop - $('.lyric').height()/3
                $('.lines').css('transform',`translateY(-${delta}px)`)
            }
        },100)
    }
    function  pad(number) {
        return number>=10 ? number + '' : '0' + number
    }
    function  initText(name,lyric) {
        $('.song-description h1').text(name)
    }
    function  parseLyric(lyric) {
        let array = lyric.split('\n')
        let regex = /^\[(.+)\](.*)$/
        // console.log(array)
        array = array.map(function (string) {
            let matches = string.match(regex)
            // console.log(matches)
            if(matches){
                return {time: matches[1],word:matches[2]}
            }
        })
        // console.log(array)
        let $lyric = $('.lyric')
        array.map(function (object) {
            if(!object){return}
            let $p = $('<p>')
            $p.attr('data-time',object.time).text(object.word)
            $p.appendTo($lyric.children('.lines'))
        })
    }


})