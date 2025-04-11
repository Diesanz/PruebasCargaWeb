<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Inicio</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
        <link rel="stylesheet" href="paginaa2.css">
    </head>

    <body>
        <header>
            <div class="movil">

                <nav>
                    <button id="bmenu"><span class="material-symbols-outlined">menu</span></button>
                    
                    <%if(usr == null){%>
                        <div class="logo-portatil"><a href="./index.jsp">EATTHIS!!</a></div>
                    <%}else{
                        String url = "./index.jsp?usr=" + usr;
                        %>
                        <div class="logo-portatil"><a href=<%=url%>>EATTHIS!!</a></div>
                    <%}%>
                    <div class="link-movil">
                        <%if(usr == null){%>
                            <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">forum</span></a>
                            <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">shopping_cart</span></a>
                            <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">account_circle</span></a>
                        <%}else{
                            String url1 = "./Chat/chat.jsp?usr=" + usr;
                            String url2 = "./Cesta/cesta.jsp?usr=" + usr;
                            String url3 = "./Perfil/cuenta.jsp?usr=" + usr;
                            %>
                            <a href=<%=url1%> class="link"><span class="material-symbols-outlined">forum</span></a>
                            <a href=<%=url2%> class="link"><span class="material-symbols-outlined">shopping_cart</span></a>
                            <a href=<%=url3%> class="link"><img src="./imagenes/persona.jpg" width="24px" height="24px" alt="alt" style="border-radius: 50%"/></a>
                        <%}%>
                    </div>
                </nav>
                <%if(usr == null){%>
                    <div class="links">
                        <a href="./Menus/menu.jsp">Menu</a>
                        <a href="./Snacks/snacks.jsp">Snacks</a>
                        <a href="./Platos/platos.jsp">Platos</a>
                        <a href="./Rutinas/rutinas.jsp">Rutinas</a>
                    </div>
                <%}else{
                    String url1 = "./Menus/menu.jsp?usr=" + usr;
                    String url2 = "./Snacks/snacks.jsp?usr=" + usr;
                    String url3 = "./Platos/platos.jsp?usr=" + usr;
                    String url4 = "./Rutinas/rutinas.jsp?usr=" + usr;
                    %>
                    <div class="links">
                        <a href=<%=url1%>>Menu</a>
                        <a href=<%=url2%>>Snacks</a>
                        <a href=<%=url3%>>Platos</a>
                        <a href=<%=url4%>>Rutinas</a>
                    </div>
                <%}%>
                

            </div>
            <div class="portatil">
                <nav>
                    <div class="arriba">
                        <%if(usr == null){%>
                            <div class="logo-portatil"><a href="./index.jsp">EATTHIS!!</a></div>
                        <%}else{
                            String url = "./index.jsp?usr=" + usr;
                            %>
                            <div class="logo-portatil"><a href=<%=url%>>EATTHIS!!</a></div>
                        <%}%>
                    </div>
                    <div class="abajo">
                        <div></div>
                        <ul>
                            <%if(usr == null){%>
                                <li><a href="./Menus/menu.jsp" class="link">Menu</a></li>
                                <li><a href="./Snacks/snacks.jsp" class="link">Snacks</a></li>
                                <li><a href="./Platos/platos.jsp" class="link">Platos</a></li>
                                <li><a href="./Rutinas/rutinas.jsp" class="link">Rutinas</a></li>
                            <%}else{
                                String url1 = "./Menus/menu.jsp?usr=" + usr;
                                String url2 = "./Snacks/snacks.jsp?usr=" + usr;
                                String url3 = "./Platos/platos.jsp?usr=" + usr;
                                String url4 = "./Rutinas/rutinas.jsp?usr=" + usr;
                                %>
                                <li><a href=<%=url1%> class="link">Menu</a></li>
                                <li><a href=<%=url2%> class="link">Snacks</a></li>
                                <li><a href=<%=url3%> class="link">Platos</a></li>
                                <li><a href=<%=url4%> class="link">Rutinas</a></li>
                            <%}%>
                            
                        </ul>
                        <div class="iconos-portatil">
                            <%if(usr == null){%>
                                <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">forum</span></a>
                                <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">shopping_cart</span></a>
                                <a href="./InicioSesion/inicioSesion.jsp" class="link"><span class="material-symbols-outlined">account_circle</span></a>
                            <%}else{
                                String url1 = "./Chat/chat.jsp?usr=" + usr;
                                String url2 = "./Cesta/cesta.jsp?usr=" + usr;
                                String url3 = "./Perfil/cuenta.jsp?usr=" + usr;
                                %>
                                <a href=<%=url1%> class="link"><span class="material-symbols-outlined">forum</span></a>
                                <a href=<%=url2%> class="link"><span class="material-symbols-outlined">shopping_cart</span></a>
                                <a href=<%=url3%> class="link"><img src="./imagenes/persona.jpg" width="24px" height="24px" alt="alt" style="border-radius: 50%"/></a>
                            <%}%>
                        </div>
                    </div>
                </nav>
            </div>
        </header>

        <section id="seccion1">
            <div class="izquierda"></div>
            <div class="derecha">
                <h2>Comer sano al mejor precio</h2>
                <ul>
                    <li><span class="material-symbols-outlined">done_all</span>Menus personalizados</li>
                    <li><span class="material-symbols-outlined">done_all</span>Snacks saludables</li>
                    <li><span class="material-symbols-outlined">done_all</span>Platos sabrosos</li>
                    <li><span class="material-symbols-outlined">done_all</span>Rutinas específicas</li>
                </ul>
                <%if(usr == null){%>
                    <a href="./Menus/menu.jsp">Haz tu pedido</a>    
                <%}else{
                    String url1 = "./Menus/menu.jsp?usr=" + usr;%>
                    <a href="./Menus/menu.jsp">Haz tu pedido</a>    
                <%}%>
            </div>
        </section>

        <section id="seccion2">
            <h2>¿Como funcionamos?</h2>
            <div class="secciondiv">
                <div class="columna1">
                    <div class="grupo">
                        <h4>1. Elige</h4>
                        <p>
                            Selecciona el plato a tu gusto,
                            seguro que te gusta.
                        </p>
                    </div>
                    <div class="grupo">
                        <h4>2. Pide</h4>
                        <p>
                            Selecciona el metodo de pago,
                            espera a que llegue
                        </p>
                    </div>
                </div>
                <div class="columna2">
                    <div class="grupo">
                        <h4>3. Recibe</h4>
                        <p>
                            Recibiras los pedidos 
                            los Lunes y Jueves
                        </p>
                    </div>
                    <div class="grupo">
                        <h4>4. Calienta</h4>
                        <p>
                            3 minutos al microondas
                            y listo para comer
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <section id="seccion3">
            <h2>Recomendaciones</h2>
            <%
                String urlDestino2;
                String urlDestino = "/eatthis/DescripcionPlato/descripcionPlato.jsp";
                if (usr == null) {
                    urlDestino = urlDestino + "?idPlato=";
                } else {
                    urlDestino = urlDestino + "?usr=" + usr + "&idPlato=";
                }

                ArrayList<Plato> listaPlatos = ServicioProductos.getListaPlatos("Equilibrado");
            %>
            <div class="secciondiv">
                <%
                    if (listaPlatos != null && !listaPlatos.isEmpty()) {
                        for (int i = 0; i < 4 && i < listaPlatos.size(); i++) {
                            Plato plato = listaPlatos.get(i); 
                            Productos p1 = ServicioProductos.getProductoFromDB(plato.getId_plato());
                            InformacionNutritiva nutrientes = ServicioProductos.selectNutrientes(plato.getId_plato());
                            String urlImagen = p1.getUrl();
                            String nombrePlato = plato.getNombre();
                            String id = String.valueOf(plato.getId_plato());
                            urlDestino2 = urlDestino + id;
                %>
                            <div class="plato">
                                <a href="<%= urlDestino2 %>" style="text-decoration: none; color:black;">
                                    <img src="<%= urlImagen %>" alt="<%= nombrePlato %>">
                                    <div class="descripcion">
                                        <h4 class="nombre"><%= nombrePlato %></h4>
                                        <div class="precio">
                                            <h4><%= p1.getPrecio() %> €</h4>
                                        </div>
                                        <div class="nutrientes">
                                            <div class="nutrientes1">
                                                <div class="nut"><p><%= nutrientes.getCalorias() %></p></div>
                                                <div class="nut"><p><%= nutrientes.getProteinas() %></p></div>
                                                <div class="nut"><p><%= nutrientes.getHidratosCarbono() %></p></div>
                                                <div class="nut"><p><%= nutrientes.getSales() %></p></div>
                                                <div class="nut"><p><%= nutrientes.getAzucares() %></p></div>
                                            </div>
                                            <div class="nutrientes2">
                                                <div class="nut"><p>KgCal</p></div>
                                                <div class="nut"><p>Proteína</p></div>
                                                <div class="nut"><p>Hidratos</p></div>
                                                <div class="nut"><p>Sales</p></div>
                                                <div class="nut"><p>Azúcares</p></div>
                                            </div>
                                        </div>
                                        <div class="botonCarro">
                                            <button class="boton1">Añadir al carro</button>
                                        </div>
                                    </div>
                                </a>    
                            </div>
                <%
                        }
                    } else {
                %>
                    <div class="no-platos">
                        <p>No hay recomendaciones disponibles en este momento.</p>
                    </div>
                <%
                    }
                %>
            </div>
        </section>


        <footer>
            <div class="footerdiv">
                <div class="grupo">
                    <h4>Descarga la app</h4>
                    <ul>
                        <li><a href="#"><span class="material-symbols-outlined">ios</span>App Store</a></li>
                        <li><a href="#"><span class="material-symbols-outlined">android</span>Play Store</a></li>
                    </ul>
                </div>
                <div class="grupo">
                    <h4>Opiniones y reseña</h4>
                    <ul>
                        <li><a href="#"><span class="material-symbols-outlined">mark_as_unread</span>Enviar opinion</a></li>
                    </ul>
                </div>
                <div class="grupo">
                    <h4>Siguenos</h4>
                    <ul>
                        <li><a href="#"><span class="material-symbols-outlined">raven</span>Twitter</a></li>
                        <li><a href="#"><span class="material-symbols-outlined">nest_heat_link_gen_3</span>Instagram</a></li>
                        <li><a href="#"><span class="material-symbols-outlined">youtube_activity</span>YouTube</a></li>
                    </ul>
                </div>
            </div>
        </footer>
        <script src="main.js" type="module"></script>
    </body>
</html>
