            const BoardSize = 11
            const RefreshRate = 15
            const PlayerColors = ["white","red","blue"];
            const BlankHexData = {board:Array.from(Array(BoardSize**2), () => 0)}


            //1st Initalization Sequence
            function initialize() {

                HexData = BlankHexData
                HexBoard = hexmapper(HexData['board']);
                console.log(HexBoard);  
                HexGameArea.start();}

            //Will be dynamically Adjustable in the future.
            //var BaseSize=(document.getElementById('CentralColumn').clientWidth)
            var BaseSize=660

            console.log("Base Size", BaseSize)

            var PieceSize =    BaseSize*(2/33)
            var CanvasHeight = BaseSize*(23/33)
            var CanvasWidth =  BaseSize
            var PieceXBias =   BaseSize*(1/66)
            var PieceYBias =   BaseSize*(1/66)

            // Makes sure requests are not sent before server has responded
            var ReadyToSend = true

            //Player Selection must be made before the first move
            var GameStart = false
            var humanplayer = 1

            function sendAJAXRequest(board,computetime,humanplayer) {
                //do not implemented stuffs
                console.log("Sent Request to Server:\n Board:",board,"\nComputetime:",computetime,"\nHumanplayer",humanplayer)
                //ReadyToSend=True
            }



            function startgame(){
                var radioplayerselector = document.getElementsByName("PlayerSelection")
                for (var i = radioplayerselector.length - 1; i >= 0; i--) {
                    if (radioplayerselector[i].checked) {
                        humanplayer = Number(radioplayerselector[i].value);
                        console.log("Game Started By User as Player",humanplayer)
                        GameStart=true}
                    radioplayerselector[i].disabled= true
                    document.getElementById("startgamebutton").disabled = true;
                }
                    if (humanplayer==2) {
                        ReadyToSend=false
                        sendAJAXRequest(HexData['board'],computetime,humanplayer)
                        //Send AJAX Request for first move
                    }}

            // Allowed Compute Time in Miliseconds, determined from a slider
            var CTSlider = document.getElementById("CTSlider");
            var CTDisp = document.getElementById("CTDisp");
            CTDisp.innerHTML = CTSlider.value;
            var computetime = Number(CTSlider.value)

            CTSlider.oninput = function() {
                CTDisp.innerHTML = this.value;
                computetime = Number(CTSlider.value);
                console.log("Client Side Compute Time Modification: Value:", computetime)
            }



            //Main Object, each cell of the board
            function hexpiece(player, pos) {
                /*
                ------
                Player
                0:White
                1:Red
                2:Blue
                ------
                Pos should be between [0,Boardsize^2)
                _x and _y are internal for plotting at right location
                */

                // Init
                this.pos = pos
                this.player = player;

                this._x = PieceSize*(Math.floor(this.pos/BoardSize))+(PieceSize/2)*(this.pos%BoardSize)+PieceXBias;
                this._y = (PieceSize*(this.pos%BoardSize))+PieceYBias;  

                // Render this object
                this.update = function() {
                    ctx = HexGameArea.context;
                    ctx.beginPath();
                    ctx.fillStyle = PlayerColors[this.player];
                    ctx.fillRect(this._x, this._y, PieceSize, PieceSize);
                    ctx.lineWidth="1";
                    ctx.strokeStyle="black";
                    ctx.rect(this._x, this._y, PieceSize, PieceSize); 
                    ctx.stroke();}

                //Click handler: checks see if mouse event was in the bounds of the piece when called
                this.clicked = function() {
                    var myleft = this._x;
                    var myright = this._x + (PieceSize);
                    var mytop = this._y;
                    var mybottom = this._y + (PieceSize);
                    var clicked = true;
                    if ((mybottom < HexGameArea.y) || (mytop > HexGameArea.y) || (myright < HexGameArea.x) || (myleft > HexGameArea.x)) {
                        clicked = false;
                    }
                    return clicked;
                }}

            //Outputs an array of hexpiece objects from primitive of JSON
            function hexmapper(primitive){
                var valueboard = new Array();
                for (var i = primitive.length - 1; i >= 0; i--) {
                    valueboard.push(new hexpiece(primitive[i],i))}
                return valueboard}

            //Update across a an array of hexpiece objects
            function mass_update(hexarray){
                for (var i = hexarray.length - 1; i >= 0; i--) {
                    hexarray[i].update()
                }}

            //Checks for click events across all objects
            function mass_click_check(hexarray,xpos,ypos) {
                if (HexGameArea.x && HexGameArea.y) {
                    for (var i = HexBoard.length - 1; i >= 0; i--) {
                        if (HexBoard[i].clicked()) {
                            console.log("Click Event At ",HexBoard[i].pos, "Value: ",HexBoard[i].player)

                            if (HexBoard[i].player==0 && ReadyToSend==true && GameStart==true) {
                                var newboard = HexData['board'];
                                newboard[HexBoard[i].pos] = humanplayer
                                console.log("Valid Move","New Board:", newboard,"Ready To Send :", ReadyToSend)
                                

                                HexBoard[i].player = humanplayer


                                ReadyToSend = false
                                sendAJAXRequest(HexData['board'],computetime,humanplayer)
                            }
                            else {
                                console.log("Invalid Move:","Ready To Send:",ReadyToSend,"GameStart:",GameStart)
                                if (GameStart==false) {
                                    alert('You must start the game before playing')
                                }
                            }                            
                        }}}}


            //2nd Initalization Sequence
            var HexGameArea = {
                canvas : document.createElement("canvas"),
                start : function() {
                    this.canvas.width = CanvasWidth;
                    this.canvas.height = CanvasHeight;

                    this.context = this.canvas.getContext("2d");
                    document.body.insertBefore(this.canvas, document.body.childNodes[0]);

                    //Define Refresh Rate
                    this.interval = setInterval(RefreshAll, RefreshRate);
                    

                    //Click Event Handlers
                    window.addEventListener('click', function (e) {
                        HexGameArea.x = e.pageX-HexGameArea.canvas.offsetLeft;
                        HexGameArea.y = e.pageY-HexGameArea.canvas.offsetTop;
                        mass_click_check(HexBoard);
                    })
             
                    window.addEventListener('touchend', function (e) {
                        HexGameArea.x = e.pageX;
                        HexGameArea.y = e.pageY;
                        mass_click_check(HexBoard);
                    })
                }, 
                clear : function(){
                    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
                }}
            //Refresh
            function RefreshAll() {
                HexGameArea.clear();
                mass_update(HexBoard);}

            //Handles Window Resize Events

            function Resize_Canvas() {
                // body...
            }