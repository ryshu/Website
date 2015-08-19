"use strict";

window.addEventListener('load', function(){
    var title = "Choisissez le moyen de paiement.";
    var choices = {
        'cash': 'Espèces',
        'card': 'Carte de crédit',
        'check': 'Chèque',
    };

    var userList = new UserList('userlist', function(user){
        var halfContribution = function(){
            if(this.isToggled()){
                console.log(user.id + " perd sa demi cotiz");
                queryJson('', {'user': user.id, 'action': 'half_contribution_delete'}, function(resp){
                    if(resp.error){
                        alert(resp.error);
                    }
                    else{
                        this.setUntoggled();
                    }
                }.bind(this));
            }
            else{
                var selector = new SelectionPopup(title, choices, function(choice){
                    console.log(user.id + " prend une demi cotiz");
                    queryJson('', {'user': user.id, 'action': 'half_contribution_add', 'mean': choice}, function(resp){
                        if(resp.error){
                            alert(resp.error);
                        }
                        else{
                            this.setToggled();
                            this.element.nextSibling.setAttribute('class', '');
                        }
                    }.bind(this));
                }.bind(this));
                selector.pop();
            }
        };

        var fullContribution = function(){
            if(this.isToggled()){
                console.log(user.id + " perd sa full cotiz");
                queryJson('', {'user': user.id, 'action': 'full_contribution_delete'}, function(resp){
                    if(resp.error){
                        alert(resp.error);
                    }
                    else{
                        this.setUntoggled();
                    }
                }.bind(this));
            }
            else{
                var selector = new SelectionPopup(title, choices, function(choice){
                    console.log(user.id + " prend une full cotiz");
                    queryJson('', {'user': user.id, 'action': 'full_contribution_add', 'mean': choice}, function(resp){
                        if(resp.error){
                            alert(resp.error);
                            this.setUntoggled();
                        }
                        else{
                            this.setToggled();
                            this.element.previousSibling.setAttribute('class', '');
                        }
                    }.bind(this));
                }.bind(this));
                selector.pop();
            }
        };

        var btnHalfContToggled = false;
        var btnFullContToggled = false;

        if(user.contribution){
            if(user.contribution == 'half') btnHalfContToggled = true;
            if(user.contribution == 'full') btnFullContToggled = true;
        }

        return [
            new UserList.UserAction('Demi cotiz', halfContribution, btnHalfContToggled),
            new UserList.UserAction('Full cotiz', fullContribution, btnFullContToggled),
        ];
    });
});
