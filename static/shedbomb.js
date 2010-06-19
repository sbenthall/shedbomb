/* 
 * A list of Items
 *
 */
var items = [];

var comparisons = []

$(document).ready(function(){
    //setup styles for initial site
    $("#comparison-page").hide();

    //adding item to the list
    //TODO: functionalize out the add and remove functions
    //      for the callbacks here
    $("#add-form").submit(function(){

        $.ajax({
            type: 'PUT',
            url: '/bomb/'+shed_id+'/answer',
            data: {
                answer : $("#new-item").val()
            }
        });
        
        addItem($("#new-item").val());
        $("#new-item").val("");
        
        return false;
    });


    //begin comparison
    $("#compare-button").click(function(){
        compareItems(); //wrapping this is avoid passing event
    });

    $("#stop-button").click(function(){
        $("#comparison-page").hide();
        showDashboard();        
    });


     for(var i = 0; i < answers.length; i++){
         addItem(answers[i]);
     }

    $("#new-item").focus()

});


/* TODO:
 * When the comparison is stopped without exhaustive comparisons,
 *   there should be the option of _completing_ the comparisons,
 *   as opposed to initiating an exhaustive comparison.
 */

function compareItems(itemPairs){
    $("#dashboard").hide();
    $("#comparison-page").show();
    
    var itemPairs = itemPairs || shuffle(pairs(items));
    
    var handlerFactory = function(item1, item2, itemPairs){
        return function(){
            comparisons.push(new Comparison(
                $(this).data("item"),
                $(this).data("item") == item1 ? item2 : item1
            ));
            comparePair(itemPairs);
        };
    };

    var comparePair = function(itemPairs){            
        if(itemPairs.length > 0){
            var pair = shuffle(itemPairs.pop());
            
            $("#comparable-alpha").html(pair[0].name).data("item",pair[0]);
            $("#comparable-beta").html(pair[1].name).data("item",pair[1]);
            
            $("div.comparable").unbind('click');
            $("div.comparable").click(handlerFactory(pair[0], pair[1], itemPairs));
            
        } else {
            $("#comparison-page").hide();
            showDashboard();
        }
    };
    
    comparePair(itemPairs);
};

function Item(item){
    this.name = item;
    this.score = 0;
};

function Comparison(winner, loser){
    this.winner = winner;
    this.loser = loser;
}

function addItem(item){
    if(!(item instanceof Item)){
        item = new Item(item);
    }

    items.push(item);

    addItemUI(item);
};

function removeItem(item){

    $.ajax({
        type: 'DELETE',
        url: "/bomb/" + shed_id + "/" + encodeURIComponent(item.name)
    });

    removeItemUI(item)
    items.splice(items.indexOf(item),1); //removes the item
}

function addItemUI(item){

    itemHtml = "<tr name='" + item.name + "'>"
        + "<td class='item-val'>" + item.name + "</td>"
        + "<td><span class='item-score'>" + item.score + "</span></td>"
        + '<td><input type="button" value="Remove" class="remove"></input></td>'
        + '<td><input type="button" value="Bomb" class="item-compare"""></input></td>'
        + "</tr>";

    itemListEntry = $(itemHtml).data("item",item);

    $("#item-table").append(itemListEntry);

    $(itemListEntry).children().children("input.remove").click(function(){
        removeItem(item);
    });

    $(itemListEntry).children("input.item-compare").click(function(){
        // 1) Remove the comparisons that are about this item
        myItem = $(this).parent().data("item");
        comparisons = $.grep(comparisons, function(comparison){
            return !(comparison.winner == myItem || comparison.loser == myItem);
        });

        // 2) Begin a round of comparisons with only item
        //    pairs that include this item.
        compareItems(shuffle($.map(items, function(item){
            return item == myItem ? null : [[item, myItem]];
        })))
    });
}

function removeItemUI(item){
    $("#item-table").children().children("tr[name="+item.name+"]").remove();
}


function showDashboard(){
    $("#item-table").children().children("tr").remove();

    var winnerTest = function(item){
        return function(comparison){
            return comparison.winner == item;
        };
    }

    $.each(items, function(idx, item){
        item.score = $.grep(comparisons, winnerTest(item)).length;
    });

    items.sort(function(a,b){
        return b.score - a.score;
    });

    $.each(items, function(idx, item){
        addItemUI(item);
    });

    $("#dashboard").show();

};


/* 
 * Input: a list LIST
 * Output: a list of all possible combinations of 2 elements
 *         in LIST
 *
 */
function pairs(list){
    var pairs = [];

    for(var i = 0; i < list.length;i++){
        for(var j = i + 1; j < list.length; j++){
            pairs.push([list[i],list[j]]);
        }
    }

    return pairs;
};


// shuffle an array
function shuffle( myArray ) {
    var i = myArray.length;
    if ( i == 0 ) return false;
    while ( --i ) {
        var j = Math.floor( Math.random() * ( i + 1 ) );
        var tempi = myArray[i];
        var tempj = myArray[j];
        myArray[i] = tempj;
        myArray[j] = tempi;
    }

    return myArray;
};
