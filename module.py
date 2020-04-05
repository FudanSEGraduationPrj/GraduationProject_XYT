from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Column,Integer,Text,DateTime

Base = declarative_base()

class Posts_Android_Java(Base):
     __tablename__="posts_android_java"
     Id = Column(Integer,nullable=False,primary_key=True)
     PostTypeId = Column(Integer)
     AcceptedAnswerId = Column(Integer)
     ParentId = Column(Integer)
     Score = Column(Integer)
     ViewCount = Column(Integer)
     Body = Column(Text)
     OwnerUserId = Column(Integer)
     OwnerDisplayName = Column(String(256))
     LastEditorUserId = Column(Integer)
     LastEditDate = Column(DateTime)
     LastActivityDate = Column(DateTime)
     Title = Column(String(256))
     Tags = Column(String(256))
     AnswerCount = Column(Integer)
     CommentCount = Column(Integer)
     FavoriteCount = Column(Integer)
     CreationDate = Column(DateTime)


     def __init__(self,id,postTypeId,acceptedAnswerId,parentId,score,viewCount,body,ownerUserId,ownerDisplayName,lastEditorUserId,lastEditDate,lastActivityDate,title,tags,answerCount,commentCount,favoriteCount,creationDate):
          self.Id = id
          self.PostTypeId = postTypeId
          self.AcceptedAnswerId = acceptedAnswerId
          self.ParentId = parentId
          self.Score = score
          self.ViewCount = viewCount
          self.Body = body
          self.OwnerUserId = ownerUserId
          self.OwnerDisplayName = ownerDisplayName
          self.LastEditorUserId = lastEditorUserId
          self.LastEditDate = lastEditDate
          self.LastActivityDate = lastActivityDate
          self.Title = title
          self.Tags = tags
          self.AnswerCount = answerCount
          self.CommentCount = commentCount
          self.FavoriteCount = favoriteCount
          self.CreationDate = creationDate

    # def get_all_javaApi_posts(session):


class XY_posts_java(Base):
     __tablename__ = "XY_posts_java"
     Id = Column(Integer, nullable=False, primary_key=True)
     PostTypeId = Column(Integer)
     AcceptedAnswerId = Column(Integer)
     ParentId = Column(Integer)
     Score = Column(Integer)
     ViewCount = Column(Integer)
     Body = Column(Text)
     OwnerUserId = Column(Integer)
     OwnerDisplayName = Column(String(256))
     LastEditorUserId = Column(Integer)
     LastEditDate = Column(DateTime)
     LastActivityDate = Column(DateTime)
     Title = Column(String(256))
     Tags = Column(String(256))
     AnswerCount = Column(Integer)
     CommentCount = Column(Integer)
     FavoriteCount = Column(Integer)
     CreationDate = Column(DateTime)

     def __init__(self, id, postTypeId, acceptedAnswerId, parentId, score, viewCount, body, ownerUserId,
                  ownerDisplayName, lastEditorUserId, lastEditDate, lastActivityDate, title, tags, answerCount,
                  commentCount, favoriteCount, creationDate):
          self.Id = id
          self.PostTypeId = postTypeId
          self.AcceptedAnswerId = acceptedAnswerId
          self.ParentId = parentId
          self.Score = score
          self.ViewCount = viewCount
          self.Body = body
          self.OwnerUserId = ownerUserId
          self.OwnerDisplayName = ownerDisplayName
          self.LastEditorUserId = lastEditorUserId
          self.LastEditDate = lastEditDate
          self.LastActivityDate = lastActivityDate
          self.Title = title
          self.Tags = tags
          self.AnswerCount = answerCount
          self.CommentCount = commentCount
          self.FavoriteCount = favoriteCount
          self.CreationDate = creationDate

class Posts_android_java_answer_index(Base):
     __tablename__ = "Posts_android_java_answer_index"
     Id = Column(Integer, nullable=False, primary_key=True)
     PostTypeId = Column(Integer)
     AcceptedAnswerId = Column(Integer)
     ParentId = Column(Integer)
     Score = Column(Integer)
     ViewCount = Column(Integer)
     Body = Column(Text)
     OwnerUserId = Column(Integer)
     OwnerDisplayName = Column(String(256))
     LastEditorUserId = Column(Integer)
     LastEditDate = Column(DateTime)
     LastActivityDate = Column(DateTime)
     Title = Column(String(256))
     Tags = Column(String(256))
     AnswerCount = Column(Integer)
     CommentCount = Column(Integer)
     FavoriteCount = Column(Integer)
     CreationDate = Column(DateTime)
     def __init__(self, id, postTypeId, acceptedAnswerId, parentId, score, viewCount, body, ownerUserId,
                  ownerDisplayName, lastEditorUserId, lastEditDate, lastActivityDate, title, tags, answerCount,
                  commentCount, favoriteCount, creationDate):
          self.Id = id
          self.PostTypeId = postTypeId
          self.AcceptedAnswerId = acceptedAnswerId
          self.ParentId = parentId
          self.Score = score
          self.ViewCount = viewCount
          self.Body = body
          self.OwnerUserId = ownerUserId
          self.OwnerDisplayName = ownerDisplayName
          self.LastEditorUserId = lastEditorUserId
          self.LastEditDate = lastEditDate
          self.LastActivityDate = lastActivityDate
          self.Title = title
          self.Tags = tags
          self.AnswerCount = answerCount
          self.CommentCount = commentCount
          self.FavoriteCount = favoriteCount
          self.CreationDate = creationDate


class Comments(Base):
    __tablename__ = "comments"
    Id = Column(Integer, nullable=False, primary_key=True)
    PostId = Column(Integer)
    Score = Column(Integer)
    CreationDate = Column(DateTime)
    UserId = Column(Integer)
    Text = Column(Text)

    def __init__(self, id, postId, score,  text, creationDate, userId):
        self.Id = id
        self.PostId = postId
        self.Score = score
        self.Text = text
        self.CreationDate = creationDate
        self.UserId = userId


class Post_Java(Base):
    __tablename__ = "post_java"
    Id = Column(Integer, nullable=False, primary_key=True)
    PostTypeId = Column(Integer)
    AcceptedAnswerId = Column(Integer)
    ParentId = Column(Integer)
    Score = Column(Integer)
    ViewCount = Column(Integer)
    Body = Column(Text)
    OwnerUserId = Column(Integer)
    LastEditorUserId = Column(Integer)
    LastEditDate = Column(DateTime)
    LastActivityDate = Column(DateTime)
    Title = Column(String(256))
    Tags = Column(String(256))
    AnswerCount = Column(Integer)
    CommentCount = Column(Integer)
    FavoriteCount = Column(Integer)
    CreationDate = Column(DateTime)

    def __init__(self, id, postTypeId, acceptedAnswerId, parentId, score, viewCount, body, ownerUserId,
             lastEditorUserId, lastEditDate, lastActivityDate, title, tags, answerCount,
                 commentCount, favoriteCount, creationDate):
        self.Id = id
        self.PostTypeId = postTypeId
        self.AcceptedAnswerId = acceptedAnswerId
        self.ParentId = parentId
        self.Score = score
        self.ViewCount = viewCount
        self.Body = body
        self.OwnerUserId = ownerUserId
        self.LastEditorUserId = lastEditorUserId
        self.LastEditDate = lastEditDate
        self.LastActivityDate = lastActivityDate
        self.Title = title
        self.Tags = tags
        self.AnswerCount = answerCount
        self.CommentCount = commentCount
        self.FavoriteCount = favoriteCount
        self.CreationDate = creationDate


class Posts_Java_And_Comments(Base):
    __tablename__ = "posts_java_and_comments"
    Id = Column(Integer, nullable=False, primary_key=True)
    PostTypeId = Column(Integer)
    AcceptedAnswerId = Column(Integer)
    ParentId = Column(Integer)
    Score = Column(Integer)
    Body = Column(Text)
    OwnerUserId = Column(Integer)
    CommentsText = Comments(Text)
    Title = Column(String(256))
    Tags = Column(String(256))
    AnswerCount = Column(Integer)
    CommentCount = Column(Integer)


    def __init__(self, id, postTypeId, acceptedAnswerId, parentId, score, body, ownerUserId,
                 title, tags, answerCount,commentCount, commentsText):
        self.Id = id
        self.PostTypeId = postTypeId
        self.AcceptedAnswerId = acceptedAnswerId
        self.ParentId = parentId
        self.Score = score
        self.Body = body
        self.OwnerUserId = ownerUserId
        self.Title = title
        self.Tags = tags
        self.AnswerCount = answerCount
        self.CommentCount = commentCount
        self.CommentsText = commentsText










