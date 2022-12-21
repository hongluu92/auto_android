<template>
  <div>
    <!-- State that the user has no permissions to view this page -->
    <h1 class="not-authorized">
      Looks like you are attempting to access a restricted page!
    </h1>
  </div>
</template>

<script>
export default {};
</script>

<style>
.not-authorized {
  text-align: center;
  margin-top: 50px;
}
</style>