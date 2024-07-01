$(function(){
    function loadUsers() {
        $.ajax({
            url: '/get_users',
            type: 'GET', 
            success: function(users) {
                const userContainer = $('#user-container');
                userContainer.empty();

                users.forEach(user => {
                    let userBox;
                    if(user.start_time !== "00:00"){ //start_time aleady exist

                        if(user.end_time !== "00:00"){ //end_time aleady exist
                            userBox = `
                                <div class="box">
                                    <img src="${user.image}">
                                    <h2>${user.username}</h2>
                                    <div>go to work:<span>${user.start_time}</span><br>
                                    leave work:<span>${user.end_time}</span>
                                    </div>
                                </div>
                            `;
                        }else{  //only start_time
                            userBox = `
                                <div class="box online">
                                    <img src="${user.image}">
                                    <h2>${user.username}</h2>
                                    <div>go to work:<span>${user.start_time}</span><br></div>
                                </div>
                            `;
                            }
                            
                    }else{ //Not going to work
                        userBox = `
                            <div class="box offline">
                                <img src="${user.image}">
                                <h2>${user.username}</h2>
                            </div>
                        `;
                    }
                    
                    userContainer.append(userBox);
                });
            },
            error: function(error) {
                console.error('Error loading users:', error);
            }
        });
    }

    loadUsers(); //users.json

    setInterval(loadUsers, 1000);  // user date update
})
