$(document).ready(function(){
   $('.video').click(function(){
        $('.frame').html('<div class="frame-close"><i class="fa-solid fa-xmark"></i></div><iframe width="100%" height="100%" src="https://www.youtube.com/embed/orbkg5JH9C8?si=AS2bxCwgppa27d6o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" id="iframe-yt" allowfullscreen></iframe>')
        $('.overlay').fadeOut(500);
        $('.overlay').css({
            'display':'flex',
        });
   });
   $('.frame-close').click(function(){
    $('.overlay').fadeIn(500);
    $('.overlay').css({
        'display':'none',
    });
    $('.frame').html(' ');
   });
    $('.overlay').click(function(){
        $(this).fadeIn(300);
        $(this).css({
            'display':'none',
    });
    }); 
    $('.overlay2').click(function(){
        $('.search-overlay').slideUp(500);
        $(this).fadeIn(500);
        $('.search-overlay').css({
            'display':'none',
        });
        $('.overlay2').css({
            'display':'none',
        });
    }); 
    $('.search-link').click(function(){
        $('.search-overlay').slideDown(500);
        $('.overlay2').fadeIn(500);
        $('.search-overlay').css({
            'display':'flex',
        });
    }); 
    $(window).scroll(function(){
        if(scrollY > 100){
            $('nav').css({
                'width':'100%',
                'backgroundColor':'rgba(0, 0, 0,0.7)',
                'backdropFilter':'blur(10px)',
            })
            $('.header-icons li a span').css({
                'color':'#fff',
            })
            $('.header-icons li a i').css({
                'color':'#fff',
            })
        }else{
            $('nav').css({
                'width':'100%',
                'backgroundColor':'transparent',
                'backdropFilter':'blur(0px)',
            })
            $('.header-icons li a span').css({
                'color':'#000',
            })
            $('.header-icons li a i').css({
                'color':'#000',
            })

        }
    });

    $('.cart-link').click(function(){
        $('.overlay2').fadeIn(500);
        $('.cart').css({
            'right':'0px',
        })
    });

    $('.overlay2').click(function(){
        $('.overlay2').fadeOut(500);
        $('.cart').css({
            'right':'-100%',
        })
    });

    $('.cart-close').click(function(){
        $('.overlay2').fadeOut(500);
        $('.cart').css({
            'right':'-100%',
        })
    });

    $('.menu-link').click(function(){
        $('.overlay2').fadeIn(500);
        $('.menu').css({
            'right':'0px',
        })
    });

    $('.overlay2').click(function(){
        $('.overlay2').fadeOut(500);
        $('.menu').css({
            'right':'-100%',
        })
    });

    $('.menu-close').click(function(){
        $('.overlay2').fadeOut(500);
        $('.menu').css({
            'right':'-100%',
        })
    });
    
    $('.ul-product li').click(function(){
        $(this).children('.text').show();
        $(this).siblings().children('.text').hide();
        $(this).children('h4').css({
            'color':'rgb(214, 156, 10)',
        })
        $(this).siblings().children('h4').css({
            'color':'#000',
        })
    });

    $('#share').click(function(){
        $('.overlay3').fadeIn(500)
        $('.overlay3').css({
            'display':'flex',
        })
        $('.link-copy').show(500)
    });

    $('.overlay3').click(function(){
        $(this).fadeOut(500)
        $('.link-copy').hide(500)
    });
    $('#close-copy-link').click(function(){
        $('.overlay3').fadeOut(500)
        $('.link-copy').hide(500)
    });
   
    
});