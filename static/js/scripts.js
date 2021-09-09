    $(document).ready(function(){
        $(".save-comment").on('click',function(){
            var _answerId=$(this).data('answer');
            var _comment=$(".comment-text-"+_answerId).val();
            // Ajax
            $.ajax({
                url:"/save-comment",
                type:"post",
                data:{
                    comment:_comment,
                    answerId:_answerId,
                    csrfmiddlewaretoken:"{{csrf_token}}"
                },
                dataType:'json',
                beforeSend:function(){
                    $(".save-comment").addClass('disabled').text('saving...');
                },
                success:function(res){
                    if(res.bool==true){
                        $(".comment-text-"+_answerId).val('');
                        // Append Element
                        var _html='<div class="card mb-2 animate__animated animate__bounce">\
                        <div class="card-body">\
                            <p>'+_comment+'</p>\
                            <p>\
                                <a href="#">{{request.user}}</a>\
                            </p>\
                        </div>\
                    </div>';
                    $(".comment-wrapper-"+_answerId).append(_html);
                    var prevCount=$(".comment-count-"+_answerId).text();
                    $(".comment-count-"+_answerId).text(parseInt(prevCount)+1);
                    }
                    $(".save-comment").removeClass('disabled').text('Submit');
                }
            });
        });
        setTimeout(function(){
            if($('message').length > 0){
                $('message').remove();
            }
        }, 200);
    });

    const answerInput = document.getElementById('id_answer')