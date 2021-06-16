<template>
    <div id="login">
        <vue-particles
                color="#292929"
                :particleOpacity="1"
                :particlesNumber="80"
                shapeType="circle"
                :particleSize="2"
                linesColor="#292929"
                :linesWidth="1"
                :lineLinked="true"
                :lineOpacity="0.8"
                :linesDistance="150"
                :moveSpeed="3"
                :hoverEffect="true"
                hoverMode="grab"
                :clickEffect="true"
                clickMode="remove"
        >
        </vue-particles>
        <Login_card id="login_card"></Login_card>

    </div>

</template>

<script>
    import Login_card from "../components/Login_card";

    export default {
        name: "Login",
        components: {
            Login_card,

        },
    }
</script>

<style scoped>
    #login{
        text-align: center;

    }

    #login_card{

        position: relative;

    }

    #particles-js{
        width: 100%;
        height: 100%;
        position: absolute;
    }
</style>