# Data

This branch is only intended to keep a backup of the `data.xml` file mentioned in the [Get Started: Data and Model Access](https://dvc.org/doc/start/data-management/access) from the [Iterative.AI dataset-registry](https://github.com/iterative/dataset-registry) GitHub repository. It is only intended to simulate the traditional approach to store and share data among the team.

The dataset contains 10K posts from StackOverflow. Each post has a title, description, tags and other information related to the post.

The initial data was obtained using the following steps:

```sh
# Clone the dataset-registry repository
git clone git@github.com:iterative/dataset-registry.git

# Switch to the cloned repository
cd dataset-registry

# Retrieve the `data.xml` file
dvc import https://github.com/iterative/dataset-registry \
  get-started/data.xml -o data.xml

# Move the `data.xml` file to this project
mv data.xml ../ml-ops-example/data.xml

# Switch back to the ML Ops example directory
cd ../ml-ops-example

# Add all the files
git add .

# Commit the changes
git commit -m "Add data"

# Push the changes
git push
```
