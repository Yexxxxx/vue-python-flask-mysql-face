<template>
    <div>
        <vue-ellipse-progress
                :progress=credit/10
                :angle="-90"
                :color="gradient"
                colorFill="#FFFFFF"
                emptyColor="#DCDCDC"
                emptyColorFill="#FFFFFF"
                :size="200"
                thickness="5"
                emptyThickness="8"
                lineMode="in"
                :legend="true"
                :legendValue='credit'
                legendClass="legend-custom-style"
                dash="0 0"
                animation="loop 700 1000"
                :loading="loading"
                fontColor="#000000"
                :gap="10"
                fontSize="20px">
            <p slot="legend-caption">信用评分</p>
        </vue-ellipse-progress>
    </div>
</template>

<script>

    export default {
        name: "X_circle",

        data(){
            return {
                loading:false,
                legendValue:'',
                gradient: {
                    radial: false,
                    colors: [
                        {
                            color: '#FF4500',
                            offset: 0,
                            opacity: '1',
                        },
                        {
                            color: '#00FF00',
                            offset: 100,
                            opacity: '1',
                        },
                    ],

                },
            }
        },
        props:['credit'],
        watch:{

        },
        created(){

        },
        computed: {

        },
        methods: {

        },
    }
</script>

<style scoped>

</style>