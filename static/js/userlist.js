'use strict';

(function(){

    var UserList = function(containerId, listProvider, buildCallback){
        BaseList.call(this, containerId, buildCallback);
        queryJson(listProvider, {}, this.populate.bind(this));
    };

    UserList.prototype = Object.create(BaseList.prototype, {
        populate: {
            value: function(json){
                this.elems = json['users'];
                for(var i in this.elems){
                    var user = this.elems[i];
                    var img = document.createElement('img');
                        img.setAttribute('src', user['picture']);
                        img.setAttribute('alt', 'profile_picture');
                    var pictureContainer = document.createElement('div');
                        pictureContainer.setAttribute('class', 'picture_container');
                    var nameContainer = document.createElement('div');
                        nameContainer.appendChild(document.createTextNode(user['display_name']));
                    var actionContainer = document.createElement('div');
                        actionContainer.setAttribute('class', 'action_container');


                    user.element = document.createElement('li');
                    user.element.appendChild(pictureContainer);
                    user.element.appendChild(nameContainer);
                    user.element.appendChild(actionContainer);
                    if(this.onElemBuild){
                        var actions = this.onElemBuild(user);
                        for(var i in actions){
                            actionContainer.appendChild(actions[i].element);
                        }
                    }
                    pictureContainer.appendChild(img);
                    this.listelement.appendChild(user.element);
                }

                this.matchingElems = this.elems;
                this.matchingElems.sort(function(a, b){
                    var nameA = a['display_name'].toLowerCase();
                    var nameB = b['display_name'].toLowerCase();

                    if(nameA > nameB) return 1;
                    else if(nameA < nameB) return -1;
                    else return 0;
                });

                this.render();
            },
        },
    });

    window.UserList = UserList;
    window.UserList.UserAction = Action;

})();
