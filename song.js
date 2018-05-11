$(function(){
     let id = location.search.match(/\bid=([^&]*)/)[1]
    console.log(id)
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
    $.get('./otherSongs.json').then(
        function (res) {
            let songs = res
            let song = songs.filter(s=>s.id_ == id)[0]
            let {id_,name,album,signer} = song
            let audio = document.createElement('audio')
            audio.src = 'http://link.hhtjim.com/163/'+id_+'.mp3'
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
        }
    )
    function initPlayer(url) {

    }
    $.get('./lyric.json').then(function(object){
        let {lyric} = object
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
    })



})