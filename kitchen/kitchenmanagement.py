from flask import Flask, jsonify, make_response, render_template, session, request, redirect, url_for
from flask.blueprints import Blueprint
from database import db

# Register this file as a Blueprint to be used in the application
kitchenmanagement = Blueprint("kitchenmanagement", __name__, static_folder="../static/", template_folder="../templates/")


@kitchenmanagement.route("/registerkitchen", methods=['POST', 'GET'])
def registerkitchen():
    try:
        if request.method == 'POST':
            name = request.form['name']
            firstline = request.form['addLine1']
            secondline = request.form['addLine2']
            city = request.form['city']
            postcode = request.form['postcode']
            country = request.form['country']
            defaultkitchen = request.form.get('defaultKitchen')
            new_kitchen = db.kitchen(nickname=name, line1=firstline, line2=secondline, city=city, postcode=postcode, country=country)      
            db.db.session.add(new_kitchen)

            currentuser = db.user.query.filter_by(user_az_id=session["user_id"]).first()
            currentuser.kitchens.append(new_kitchen)
            #thing = db.user_kitchen(filter(lambda x: x.kitchen_id == new_kitchen.kitchen_id, currentuser.kitchen_associations)) #.query.filter_by(kitchen_id=new_kitchen.kitchen_id).first()

            if defaultkitchen:
                notdefaultkitchen = db.db.session.query(db.user_kitchen).filter( 
                    db.user_kitchen.user_id == currentuser.user_id,
                    db.user_kitchen.is_default_kitchen == True).first()
                notdefaultkitchen.is_default_kitchen = False

                userkitchens = db.db.session.query(db.user_kitchen).filter(
                    db.user_kitchen.kitchen_id == new_kitchen.kitchen_id, 
                    db.user_kitchen.user_id == currentuser.user_id).first()
                userkitchens.is_default_kitchen = True
            else:
                userkitchens = db.db.session.query(db.user_kitchen).filter(
                    db.user_kitchen.kitchen_id == new_kitchen.kitchen_id, 
                    db.user_kitchen.user_id == currentuser.user_id).first()
                userkitchens.is_default_kitchen = False

            db.db.session.commit()
            """
            if defaultkitchen:
                #currentdefaultkitchen = db.session.query(user_id = currentuser.user_id, is_default_kitchen=True)
                #currentdefaultkitchen.is_default_kitchen = False
                stuff = db.db.session.query(db.user_kitchen).all()
                db.db.update(db.user_kitchen).where(db.user_kitchen.user_id == currentuser.user_id, db.user_kitchen.is_default_kitchen == True ).values(is_default_kitchen = False)
                #newuserkitchen = db.db.user_kitchen.query.filter_by(user_id = currentuser.user_id, kitchen_id = new_kitchen.kitchen_id).first()
                #newuserkitchen.is_default_kitchen = True
                db.db.session.commit()
            """
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=new_kitchen.kitchen_id))
        else:
            return render_template("registerkitchen.html")
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/showkitchen/<string:kitchid>", methods=['GET'])
def showkitchen(kitchid):
    try:
        kitchen = db.kitchen.query.filter_by(kitchen_id=kitchid).first()
        kitchenappliances = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid).all()
        kitchenovens = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=1).all()
        kitchenfridges = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=2).all()
        kitchenscales = db.kitchen_appliance.query.filter_by(kitchen_id=kitchid, kitchen_appliance_type_id=3).all()
        user = db.user.query.filter_by(user_az_id=session['user_id']).first()
        print(user)
        kid=kitchen.kitchen_id
        uid=user.user_id

        query =  db.db.session.query(db.user_kitchen).filter(
            db.user_kitchen.kitchen_id == kid, 
            db.user_kitchen.user_id == uid)

        print(query)
        
        userkitchens = db.db.session.query(db.user_kitchen).filter(
            db.user_kitchen.kitchen_id == kid, 
            db.user_kitchen.user_id == uid).first()
        #query = 'SELECT * from user_kitchen where kitchen_id = {} AND user_id = {}'.format(kitchid, user.user_id)
        #stuff = db.db.session.execute(query)
        #kitchenuser = db.kitchen.query.join(db.user_kitchen).join(db.kitchen).filter((db.user_kitchen.c.kitchen_id==kitchid)).all()
        if not kitchen:
            return redirect('/')
        isdefaultkitchen = userkitchens.is_default_kitchen
        return render_template("showkitchen.html", kitchen=kitchen, isdefaultkitchen=isdefaultkitchen, ovens=kitchenovens, fridges=kitchenfridges, scales=kitchenscales)#, kitchenuser=kitchenuser)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createoven", methods=['POST', 'GET'])
def createoven():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            new_oven = db.kitchen_appliance(nickname=name, kitchen_id=selectedkitchen, kitchen_appliance_type_id=1)
            db.db.session.add(new_oven)
            db.db.session.commit()
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = db.kitchen.query.join(db.user_kitchen).filter(db.user_kitchen.c.user_id==2).all()
            return render_template("createoven.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@kitchenmanagement.route("/showoven/<int:ovenid>", methods=['POST', 'GET'])
def showoven(ovenid):
    try:
        if request.method == 'POST':
            pass
        else:
            oven = db.kitchen_appliance.query.filter_by(kitchen_appliance_id=ovenid).first()
            kitchen = db.kitchen.query.filter_by(kitchen_id=oven.kitchen_id).first()
            return render_template("showoven.html", ovendetails=oven, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createfridge", methods=['POST', 'GET'])
def createfridge():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            new_fridge = db.kitchen_appliance(nickname=name, kitchen_id=selectedkitchen, kitchen_appliance_type_id=2)
            db.db.session.add(new_fridge)
            db.db.session.commit()
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = db.kitchen.query.join(db.user_kitchen).filter(db.user_kitchen.c.user_id==2).all()
            return render_template("createfridge.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)

@kitchenmanagement.route("/showfridge/<int:fridgeid>", methods=['POST', 'GET'])
def showfridge(fridgeid):
    try:
        if request.method == 'POST':
            pass
        else:
            oven = db.kitchen_appliance.query.filter_by(kitchen_appliance_id=fridgeid).first()
            kitchen = db.kitchen.query.filter_by(kitchen_id=oven.kitchen_id).first()
            return render_template("showfridge.html", fridgedetails=oven, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/createscale", methods=['POST', 'GET'])
def createscale():
    try:
        if request.method == 'POST':
            name = request.form['name']
            selectedkitchen = request.form.get('kitchenid')
            new_scale = db.kitchen_appliance(nickname=name, kitchen_id=selectedkitchen, kitchen_appliance_type_id=3)
            db.db.session.add(new_scale)
            db.db.session.commit()
            return redirect(url_for('kitchenmanagement.showkitchen', kitchid=selectedkitchen))
        else:
            kitchens = db.kitchen.query.join(db.user_kitchen).filter(db.user_kitchen.c.user_id==2).all()
            return render_template("createscale.html", kitchens=kitchens)

    except Exception as e:
        return render_template("errorpage.html", errorstack=e)


@kitchenmanagement.route("/showscale/<int:scaleid>", methods=['POST', 'GET'])
def showscale(scaleid):
    try:
        if request.method == 'POST':
            pass
        else:
            scale = db.kitchen_appliance.query.filter_by(kitchen_appliance_id=scaleid).first()
            kitchen = db.kitchen.query.filter_by(kitchen_id=scale.kitchen_id).first()
            return render_template("showfridge.html", scaledetails=scale, kitchendetails=kitchen)
    except Exception as e:
        return render_template("errorpage.html", errorstack=e)