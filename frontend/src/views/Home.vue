<template>

    <DHeader/>

    <PhotoList/>

    <DFooter/>

</template>

<script>
    import DHeader from '@/components/DHeader.vue'
    import DFooter from '@/components/DFooter.vue'
    import PhotoList from '@/components/PhotoList.vue'

    export default {
        name: 'Home',
        components: { DHeader, DFooter, PhotoList}
    }
</script>
