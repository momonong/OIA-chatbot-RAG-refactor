$(document).ready(() => {
    console.log('Document ready');

    // try {
    //     const Table = new DataTable('#table', {
    //         lengthMenu: [[10, 25, 50, -1], [10, 25, 50, 'All']],
    //         scrollCollapse: true,
    //         ordering: true,
    //         autoWidth: false, 
    //         scrollX: true, 
    //     });
    //     console.log('DataTable initialized');
    // } catch (error) {
    //     console.error('Error initializing DataTable:', error);
    // }

    $('.chatbot-status, .human-service').change(function() {
        console.log('Checkbox changed');
        const userId = $(this).data('user-id');
        const isChatbotStatus = $(this).hasClass('chatbot-status');
        const isChecked = $(this).prop('checked');

        // 檢查是否為人工服務複選框，且狀態從 true 變為 false
        if (!isChatbotStatus && !isChecked) {
            // 將 Chatbot 開啟狀態設為 true（僅在前端更新）
            $('.chatbot-status[data-user-id="' + userId + '"]').prop('checked', true);
        }

        $.ajax({
            url: '/update-status',
            method: 'POST',
            data: JSON.stringify({
                user_id: userId,
                status_type: isChatbotStatus ? 'chatbot' : 'human_service',
                status: isChecked
            }),
            contentType: 'application/json',
            success: function(response) {
                console.log('狀態更新成功', response);
            },
            error: function(error) {
                console.error('狀態更新失敗', error);
                $(this).prop('checked', !isChecked);
                // 如果是人工服務狀態更新失敗，恢復 Chatbot 狀態
                if (!isChatbotStatus && !isChecked) {
                    $('.chatbot-status[data-user-id="' + userId + '"]').prop('checked', false);
                }
            }
        });
    });
});

console.log('OIA.js loaded');
